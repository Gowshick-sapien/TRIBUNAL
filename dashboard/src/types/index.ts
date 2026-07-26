/**
 * TRIBUNAL REST API Data Contracts & TypeScript Definitions
 */

export interface ExecutionOptions {
  confidence_threshold?: number;
  max_depth?: number;
  include_graph?: boolean;
  include_raw_transactions?: boolean;
  expert_override?: string[];
}

export interface InvestigationRequest {
  query: string;
  dataset?: string;
  options?: ExecutionOptions;
  metadata?: Record<string, any>;
}

export interface InvestigationResponse {
  investigation_id: string;
  query: string;
  risk_level: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
  confidence: number;
  verdict: 'LIKELY_MALICIOUS' | 'POSSIBLY_MALICIOUS' | 'LIKELY_LEGITIMATE' | 'INCONCLUSIVE';
  winning_hypothesis: string;
  recommendation: string;
  summary: string;
  report_url: string;
  graph_url: string;
  verdict_url: string;
  metrics: {
    planner_ms?: number;
    experts_ms?: number;
    graph_ms?: number;
    tribunal_ms?: number;
    report_ms?: number;
    total_ms?: number;
  };
  created_at?: string;
}

export interface QueryRequest {
  query: string;
  dataset?: string;
}

export interface QueryResponse {
  query: string;
  verdict: string;
  risk_level: string;
  confidence: number;
  winning_hypothesis: string;
  recommendation: string;
  short_answer: string;
  invoked_experts: string[];
}

export interface ReportSectionSchema {
  title: string;
  order: number;
  content: string;
}

export interface ReportResponse {
  report_id: string;
  investigation_id: string;
  generated_at: string;
  version: string;
  markdown_content: string;
  html_content?: string;
  sections: ReportSectionSchema[];
  json_payload: Record<string, any>;
  risk_level: string;
  recommendation: string;
}

export interface NodeSchema {
  id: string;
  label: string;
  type: string;
  risk_score: number;
  attributes: Record<string, any>;
}

export interface EdgeSchema {
  source: string;
  target: string;
  relation: string;
  weight: number;
  attributes: Record<string, any>;
}

export interface GraphStatsSchema {
  node_count: number;
  edge_count: number;
  density: number;
  pattern_clusters: number;
}

export interface GraphResponse {
  investigation_id: string;
  nodes: NodeSchema[];
  edges: EdgeSchema[];
  statistics: GraphStatsSchema;
}

export interface VerdictResponse {
  investigation_id: string;
  verdict: string;
  winning_hypothesis: string;
  winning_score: number;
  confidence: number;
  confidence_gap: number;
  runner_up_hypothesis?: string;
  runner_up_confidence?: number;
  recommendation: string;
  deliberation_trace: Array<{
    step_number: number;
    stage_name: string;
    decision_id: string;
    step_duration_ms: number;
    description: string;
    data: Record<string, any>;
    timestamp: string;
  }>;
  reasoning_metadata: Record<string, any>;
}

export interface InvestigationRecordSchema {
  id: string;
  query: string;
  dataset: string;
  created_at: string;
  planner_intent: string;
  risk_level: string;
  confidence: number;
  recommendation: string;
  status: string;
  duration_ms: number;
  version: string;
}

export interface InvestigationListResponse {
  total: number;
  limit: number;
  offset: number;
  investigations: InvestigationRecordSchema[];
}

export interface InvestigationDetailResponse {
  record: InvestigationRecordSchema;
  report_url: string;
  graph_url: string;
  verdict_url: string;
  has_case_file: boolean;
}

export interface DatasetItemSchema {
  id: string;
  name: string;
  description: string;
  default: boolean;
}

export interface DatasetListResponse {
  datasets: DatasetItemSchema[];
  total: number;
}

export interface HealthResponse {
  status: string;
  version: string;
  api_version: string;
  uptime_seconds: number;
  planner_ready: boolean;
  engine_ready: boolean;
  timestamp: string;
}

export interface MetadataResponse {
  title: string;
  version: string;
  api_version: string;
  supported_experts: string[];
  supported_aml_patterns: string[];
  build_information: Record<string, any>;
  timestamp: string;
}
