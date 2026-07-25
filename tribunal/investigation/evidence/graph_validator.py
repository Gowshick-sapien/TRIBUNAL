"""Graph Validator module — Validates cards and EvidenceGraph structural integrity."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tribunal.models.evidence_graph import EvidenceGraph
    from tribunal.models.investigation_card import InvestigationCard

logger = logging.getLogger("tribunal.investigation.evidence.validator")

VALID_EXPERTS = {"financial", "behaviour", "network", "regulatory", "defense", "tribunal", "system"}


class GraphValidator:
    """Validates input cards and structural integrity of the generated EvidenceGraph."""

    def validate_card(self, card: InvestigationCard) -> bool:
        """Validate an InvestigationCard before inserting into graph."""
        if not card.card_id or not isinstance(card.card_id, str):
            logger.warning(f"Card rejected: invalid card_id '{card.card_id}'")
            return False

        if card.source_expert not in VALID_EXPERTS:
            logger.warning(f"Card '{card.card_id}' rejected: invalid source_expert '{card.source_expert}'")
            return False

        if card.confidence is None or not (0.0 <= card.confidence <= 1.0):
            logger.warning(f"Card '{card.card_id}' rejected: invalid confidence score '{card.confidence}'")
            return False

        if not card.provenance and not card.derived_from_transactions:
            logger.warning(f"Card '{card.card_id}' rejected: missing provenance")
            return False

        return True

    def validate_graph(self, evidence_graph: EvidenceGraph) -> bool:
        """Validate structural integrity of an EvidenceGraph."""
        if not evidence_graph or not evidence_graph.nodes:
            logger.warning("Graph validation failed: graph is empty")
            return False

        node_ids = {n.node_id for n in evidence_graph.nodes}

        # Check for dangling edges
        for edge in evidence_graph.edges:
            if edge.source not in node_ids:
                logger.error(f"Graph validation failed: edge source '{edge.source}' not in nodes")
                return False
            if edge.target not in node_ids:
                logger.error(f"Graph validation failed: edge target '{edge.target}' not in nodes")
                return False

        # Verify all nodes have valid non-negative confidence
        for node in evidence_graph.nodes:
            if node.confidence < 0.0 or node.confidence > 1.0:
                logger.error(f"Graph validation failed: node '{node.node_id}' has invalid confidence {node.confidence}")
                return False

        return True
