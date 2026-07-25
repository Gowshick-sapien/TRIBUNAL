"""Hypothesis Extractor module — Collects and categorizes hypotheses from EvidenceGraph."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from tribunal.models.evidence_graph import EvidenceGraph


@dataclass
class ExtractedHypothesis:
    hypothesis_id: str
    title: str
    account_ids: list[str]
    supporting_card_ids: list[str] = field(default_factory=list)
    defense_card_ids: list[str] = field(default_factory=list)
    expert_sources: list[str] = field(default_factory=list)
    is_defense_hypothesis: bool = False
    cards_metadata: list[dict[str, Any]] = field(default_factory=list)


class HypothesisExtractor:
    """Extracts hypothesis nodes and their supporting/opposing cards from EvidenceGraph."""

    def extract(self, graph: EvidenceGraph) -> list[ExtractedHypothesis]:
        """Traverse graph and return all extracted candidate hypotheses."""
        extracted: list[ExtractedHypothesis] = []
        if graph is None or len(graph.nodes) == 0:
            return extracted

        nx_graph = graph._graph

        for node_id, data in nx_graph.nodes(data=True):
            n_type = data.get("node_type") or data.get("type")
            if n_type != "hypothesis" and not node_id.startswith("hyp_"):
                continue

            title = data.get("label") or data.get("title") or node_id
            expert_src = data.get("expert") or data.get("source_expert") or "unknown"
            is_defense = (expert_src == "defense") or ("Legitimate" in title) or ("alternative" in node_id.lower())

            supporting_card_ids: list[str] = []
            defense_card_ids: list[str] = []
            expert_sources: set[str] = set()
            account_ids: set[str] = set()
            cards_meta: list[dict[str, Any]] = []

            # In-edges to this hypothesis node (e.g. Card -SUPPORTS-> Hypothesis)
            for in_node, _, edge_data in nx_graph.in_edges(node_id, data=True):
                in_node_data = nx_graph.nodes[in_node]
                in_type = in_node_data.get("node_type") or in_node_data.get("type")
                if in_type == "card" or in_node.startswith("card_"):
                    c_id = in_node
                    c_expert = in_node_data.get("expert") or in_node_data.get("source_expert", "")
                    if c_expert:
                        expert_sources.add(c_expert)

                    card_meta = in_node_data.get("metadata", {}).get("card") or in_node_data.get("card")
                    conf = float(in_node_data.get("confidence", 0.5))
                    sev = in_node_data.get("severity", "MEDIUM")

                    if card_meta:
                        conf = getattr(card_meta, "confidence", conf)
                        sev = getattr(card_meta, "severity", sev)
                        c_expert = getattr(card_meta, "source_expert", c_expert)

                    cards_meta.append({
                        "card_id": c_id,
                        "source_expert": c_expert,
                        "confidence": conf,
                        "hypothesis": title,
                        "severity": sev,
                    })

                    if c_expert == "defense":
                        defense_card_ids.append(c_id)
                    else:
                        supporting_card_ids.append(c_id)

                    # Trace back account nodes connected to this card (e.g. Account -HAS_EVIDENCE-> Card)
                    for acc_node, _, _ in nx_graph.in_edges(c_id, data=True):
                        acc_data = nx_graph.nodes[acc_node]
                        acc_type = acc_data.get("node_type") or acc_data.get("type")
                        if acc_type == "account" or acc_node.startswith("acc_"):
                            account_ids.add(acc_node.replace("acc_", ""))

            if expert_src:
                expert_sources.add(expert_src)

            extracted.append(
                ExtractedHypothesis(
                    hypothesis_id=node_id,
                    title=title,
                    account_ids=sorted(list(account_ids)),
                    supporting_card_ids=supporting_card_ids,
                    defense_card_ids=defense_card_ids,
                    expert_sources=sorted(list(expert_sources)),
                    is_defense_hypothesis=is_defense,
                    cards_metadata=cards_meta,
                )
            )

        return extracted
