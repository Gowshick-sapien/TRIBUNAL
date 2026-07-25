"""Evidence Graph Builder module — Main orchestrator constructing validated EvidenceGraph instances."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING

from tribunal.investigation.evidence.evidence_linker import EvidenceLinker
from tribunal.investigation.evidence.evidence_merger import EvidenceMerger
from tribunal.investigation.evidence.graph_metrics import GraphMetrics
from tribunal.investigation.evidence.graph_validator import GraphValidator
from tribunal.investigation.evidence.provenance_manager import ProvenanceManager
from tribunal.models.evidence_graph import EvidenceGraph

if TYPE_CHECKING:
    from tribunal.models.case_file import CaseFile
    from tribunal.models.execution_plan import ExecutionPlan
    from tribunal.models.investigation_card import InvestigationCard

logger = logging.getLogger("tribunal.investigation.evidence.builder")

DEFAULT_GRAPH_PATH = Path("tribunal/datasets/processed/evidence_graph.gpickle")


class EvidenceGraphBuilder:
    """Builds, validates, metrics-profiles, and persists an EvidenceGraph from expert cards."""

    def __init__(
        self,
        validator: GraphValidator | None = None,
        merger: EvidenceMerger | None = None,
        linker: EvidenceLinker | None = None,
        metrics_calculator: GraphMetrics | None = None,
    ):
        self.validator = validator or GraphValidator()
        self.merger = merger or EvidenceMerger()
        self.linker = linker or EvidenceLinker()
        self.metrics_calculator = metrics_calculator or GraphMetrics()

    def build(
        self,
        cards: list[InvestigationCard],
        case_file: CaseFile | None = None,
        execution_plan: ExecutionPlan | None = None,
    ) -> EvidenceGraph:
        """Construct a validated EvidenceGraph from input InvestigationCard objects."""
        logger.info(f"EvidenceGraphBuilder building graph from {len(cards)} input card(s)...")

        # Stage 1: Validate input cards
        valid_cards = [c for c in cards if self.validator.validate_card(c)]
        if not valid_cards:
            logger.warning("No valid cards passed validation. Returning empty EvidenceGraph.")
            eg = EvidenceGraph()
            eg.metrics = self.metrics_calculator.compute_metrics(eg)
            return eg

        # Stage 2: Merge duplicate cards
        merged_cards = self.merger.merge_cards(valid_cards)

        # Stage 3 & 4: Link nodes & infer relationships
        nodes, edges = self.linker.generate_nodes_and_edges(merged_cards)

        # Stage 5: Construct graph container & compute metrics
        metadata = {
            "case_id": case_file.case_id if case_file else "standalone",
            "input_cards_count": len(cards),
            "merged_cards_count": len(merged_cards),
        }

        evidence_graph = EvidenceGraph(nodes=nodes, edges=edges, metadata=metadata)

        # Compute graph metrics
        evidence_graph.metrics = self.metrics_calculator.compute_metrics(evidence_graph)

        # Stage 6: Validate final graph structural integrity
        is_valid = self.validator.validate_graph(evidence_graph)
        if not is_valid:
            logger.error("EvidenceGraph structural validation failed!")

        logger.info(
            f"EvidenceGraph successfully built: {len(nodes)} nodes, {len(edges)} edges, "
            f"density={evidence_graph.metrics.get('graph_density', 0)}."
        )
        return evidence_graph

    def augment_graph(
        self,
        evidence_graph: EvidenceGraph,
        defense_cards: list[InvestigationCard],
    ) -> EvidenceGraph:
        """Augment an existing EvidenceGraph with Defense Investigation Cards (Phase C.5)."""
        if not defense_cards:
            return evidence_graph

        valid_def_cards = [c for c in defense_cards if self.validator.validate_card(c)]
        if not valid_def_cards:
            return evidence_graph

        def_nodes, def_edges = self.linker.generate_nodes_and_edges(valid_def_cards)

        existing_node_ids = {n.node_id for n in evidence_graph.nodes}
        for n in def_nodes:
            if n.node_id not in existing_node_ids:
                evidence_graph.nodes.append(n)
                evidence_graph._graph.add_node(n.node_id, **n.to_dict())

        existing_edge_keys = {(e.source, e.target, e.relationship) for e in evidence_graph.edges}
        for e in def_edges:
            edge_key = (e.source, e.target, e.relationship)
            if edge_key not in existing_edge_keys:
                evidence_graph.edges.append(e)
                evidence_graph._graph.add_edge(e.source, e.target, **e.to_dict())

        # Recompute graph metrics
        evidence_graph.metrics = self.metrics_calculator.compute_metrics(evidence_graph)
        return evidence_graph

    def validate(self, evidence_graph: EvidenceGraph) -> bool:
        """Validate an EvidenceGraph."""
        return self.validator.validate_graph(evidence_graph)

    def save(self, evidence_graph: EvidenceGraph, filepath: str | Path = DEFAULT_GRAPH_PATH) -> None:
        """Save EvidenceGraph to file."""
        evidence_graph.save(filepath)
        logger.info(f"EvidenceGraph persisted to {filepath}")

    def load(self, filepath: str | Path = DEFAULT_GRAPH_PATH) -> EvidenceGraph:
        """Load EvidenceGraph from file."""
        return EvidenceGraph.load(filepath)

