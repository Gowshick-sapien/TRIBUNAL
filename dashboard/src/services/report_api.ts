import axios from 'axios';
import { getApiBaseUrl } from './api';
import type { ReportAnnotation, StructuredReportPayload } from '../types/report';

const createClient = () => {
  return axios.create({
    baseURL: getApiBaseUrl(),
    headers: { 'Content-Type': 'application/json' },
    timeout: 30000,
  });
};

export const reportApi = {
  async getReport(id: string): Promise<StructuredReportPayload> {
    const client = createClient();
    const res = await client.get<StructuredReportPayload>(`/report/${id}`);
    return res.data;
  },

  async getAnnotations(id: string): Promise<ReportAnnotation[]> {
    const client = createClient();
    const res = await client.get<ReportAnnotation[]>(`/reports/${id}/annotations`);
    return res.data;
  },

  async addAnnotation(id: string, author: string, text: string): Promise<ReportAnnotation> {
    const client = createClient();
    const res = await client.post<ReportAnnotation>(`/reports/${id}/annotations`, { author, text });
    return res.data;
  },

  async deleteAnnotation(id: string, noteId: number): Promise<void> {
    const client = createClient();
    await client.delete(`/reports/${id}/annotations/${noteId}`);
  },

  getExportUrl(id: string, format: 'markdown' | 'html' | 'pdf' | 'json' = 'markdown'): string {
    const base = getApiBaseUrl();
    return `${base}/report/${id}?format=${format}`;
  },
};
