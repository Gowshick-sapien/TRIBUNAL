import { api } from './api';
import type { EvidenceGraphPayload, GraphNodeData, GraphEdgeData } from '../types/graph';

export const graphApi = {
  async getEvidenceGraph(investigationId: string): Promise<EvidenceGraphPayload> {
    const raw = await api.getGraph(investigationId);

    // Transform API node/edge schemas into rich GraphNodeData/GraphEdgeData objects
    const nodes: GraphNodeData[] = raw.nodes.map((n) => {
      const attrs = n.attributes || {};
      let nodeType = (n.type || 'card').toLowerCase() as any;
      if (n.id.includes('tribunal') || n.label.toLowerCase().includes('verdict')) {
        nodeType = 'tribunal';
      } else if (n.id.includes('defense') || attrs.counter_hypothesis) {
        nodeType = 'defense';
      } else if (n.id.includes('gap') || attrs.missing_data) {
        nodeType = 'evidence_gap';
      }

      let severity: any = attrs.severity || 'MEDIUM';
      if (n.risk_score >= 0.85) severity = 'CRITICAL';
      else if (n.risk_score >= 0.65) severity = 'HIGH';

      return {
        id: n.id,
        label: n.label || n.id,
        type: nodeType,
        expert: attrs.expert || attrs.source_expert || (n.id.includes('beh') ? 'behaviour' : 'financial'),
        hypothesis: attrs.hypothesis || n.label,
        confidence: n.risk_score,
        risk_score: n.risk_score,
        severity: severity,
        transaction_ids: attrs.transaction_ids || attrs.transactions || [],
        counter_hypothesis: attrs.counter_hypothesis,
        rebuttal_status: attrs.rebuttal_status,
        missing_data_type: attrs.missing_data_type,
        generated_at: attrs.generated_at,
        provenance: attrs.provenance || {},
        attributes: attrs,
        isWinningPath: Boolean(attrs.is_winning_path || attrs.winning_chain),
      };
    });

    const edges: GraphEdgeData[] = raw.edges.map((e, idx) => {
      const rel = (e.relation || 'SUPPORT').toUpperCase() as any;
      const attrs = e.attributes || {};
      return {
        id: `e_${e.source}_${e.target}_${idx}`,
        source: e.source,
        target: e.target,
        relation: rel,
        weight: e.weight || 1.0,
        reasoning: attrs.reasoning || attrs.reason || `Relation ${rel} with weight ${e.weight}`,
        created_by: attrs.created_by || 'EvidenceGraphBuilder',
        attributes: attrs,
        isWinningPath: Boolean(attrs.is_winning_path || rel === 'WINNING_PATH'),
      };
    });

    return {
      investigation_id: raw.investigation_id,
      nodes,
      edges,
      statistics: {
        node_count: raw.statistics.node_count,
        edge_count: raw.statistics.edge_count,
        density: raw.statistics.density,
        pattern_clusters: raw.statistics.pattern_clusters,
        connected_components: 1,
        average_degree: raw.statistics.node_count > 0 ? (raw.statistics.edge_count * 2) / raw.statistics.node_count : 0,
        support_edges: edges.filter((e) => e.relation === 'SUPPORT').length,
        contradiction_edges: edges.filter((e) => e.relation === 'CONTRADICTION').length,
      },
    };
  },
};
