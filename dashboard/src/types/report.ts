/**
 * TRIBUNAL Interactive Report Data Contracts
 */

export interface ReportSectionItem {
  title: string;
  order: number;
  content: string;
}

export interface StructuredReportPayload {
  report_id: string;
  investigation_id: string;
  generated_at: string;
  version: string;
  markdown_content: string;
  html_content?: string;
  sections: ReportSectionItem[];
  json_payload: Record<string, any>;
  risk_level: string;
  recommendation: string;
  confidence?: number;
}

export interface ReportAnnotation {
  id: number;
  investigation_id: string;
  author: string;
  text: string;
  created_at: string;
}

export interface EvidenceCardItem {
  id: string;
  expert: string;
  hypothesis: string;
  confidence: number;
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
  supporting_transactions: string[];
}

export interface DefenseItem {
  counter_hypothesis: string;
  status: 'ACCEPTED' | 'REJECTED';
  reasoning: string;
  confidence: number;
}
