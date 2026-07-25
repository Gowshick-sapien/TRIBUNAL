"""GraphBuilder alias — redirects to EvidenceGraphBuilder."""

from tribunal.investigation.evidence.evidence_graph_builder import EvidenceGraphBuilder as GraphBuilder
from tribunal.investigation.evidence.evidence_graph_builder import EvidenceGraphBuilder

__all__ = ["GraphBuilder", "EvidenceGraphBuilder"]
