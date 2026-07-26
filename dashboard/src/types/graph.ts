/**
 * TRIBUNAL Evidence Graph Interactive Visualization Data Contracts
 */

export type GraphNodeType = 'card' | 'tribunal' | 'defense' | 'evidence_gap';
export type GraphEdgeRelation = 'SUPPORT' | 'CONTRADICTION' | 'REFERENCE' | 'WINNING_PATH';
export type SeverityLevel = 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';

export interface GraphNodeData {
  id: string;
  label: string;
  type: GraphNodeType;
  expert?: string;
  hypothesis?: string;
  confidence?: number;
  risk_score?: number;
  severity?: SeverityLevel;
  transaction_ids?: string[];
  counter_hypothesis?: string;
  rebuttal_status?: string;
  missing_data_type?: string;
  generated_at?: string;
  provenance?: Record<string, any>;
  attributes?: Record<string, any>;
  isWinningPath?: boolean;
  isDimmed?: boolean;
  [key: string]: any;
}

export interface GraphEdgeData {
  id: string;
  source: string;
  target: string;
  relation: GraphEdgeRelation;
  weight: number;
  reasoning?: string;
  created_by?: string;
  attributes?: Record<string, any>;
  isWinningPath?: boolean;
  isDimmed?: boolean;
  [key: string]: any;
}

export interface EvidenceGraphPayload {
  investigation_id: string;
  nodes: GraphNodeData[];
  edges: GraphEdgeData[];
  statistics: {
    node_count: number;
    edge_count: number;
    density: number;
    pattern_clusters: number;
    connected_components?: number;
    average_degree?: number;
    support_edges?: number;
    contradiction_edges?: number;
  };
}

export interface GraphFilterOptions {
  expertFilter: string;
  severityFilter: string;
  relationFilter: string;
  showWinningPathOnly: boolean;
  searchQuery: string;
}
