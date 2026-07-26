/**
 * TRIBUNAL Repository Explorer & Search Data Contracts
 */

export interface SearchResultItem {
  id: string;
  created_at: string;
  query: string;
  dataset: string;
  planner_intent: string;
  risk_level: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
  confidence: number;
  recommendation: string;
  status: string;
  duration_ms: number;
  version: string;
  winning_hypothesis?: string;
  is_bookmarked: boolean;
  tags: string[];
  node_count: number;
  edge_count: number;
}

export interface SearchResponse {
  total: number;
  limit: number;
  offset: number;
  results: SearchResultItem[];
}

export interface SimilarItemSchema {
  item: SearchResultItem;
  similarity_score: number;
  similarity_reasons: string[];
}

export interface SimilarListResponse {
  target_id: string;
  similar: SimilarItemSchema[];
}

export interface SearchFilterState {
  query: string;
  risk_level: string; // 'ALL' | 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW'
  min_confidence: number;
  max_confidence: number;
  dataset: string;
  status: string;
  start_date?: string;
  end_date?: string;
  only_bookmarked: boolean;
  sort_by: string; // 'newest' | 'oldest' | 'confidence_desc' | 'risk_desc' | 'fastest'
}
