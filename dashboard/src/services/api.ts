import axios from 'axios';
import type {
  DatasetListResponse,
  GraphResponse,
  HealthResponse,
  InvestigationDetailResponse,
  InvestigationListResponse,
  InvestigationRequest,
  InvestigationResponse,
  MetadataResponse,
  QueryRequest,
  QueryResponse,
  ReportResponse,
  VerdictResponse,
} from '../types';

const STORAGE_KEY = 'tribunal_api_base_url';
export const DEFAULT_API_BASE = 'http://127.0.0.1:8000/api/v1';

export const getApiBaseUrl = (): string => {
  return localStorage.getItem(STORAGE_KEY) || DEFAULT_API_BASE;
};

export const setApiBaseUrl = (url: string): void => {
  localStorage.setItem(STORAGE_KEY, url);
};

const createApiClient = () => {
  return axios.create({
    baseURL: getApiBaseUrl(),
    headers: {
      'Content-Type': 'application/json',
    },
    timeout: 30000,
  });
};

export const api = {
  async getHealth(): Promise<HealthResponse> {
    const client = createApiClient();
    const res = await client.get<HealthResponse>('/health');
    return res.data;
  },

  async getMetadata(): Promise<MetadataResponse> {
    const client = createApiClient();
    const res = await client.get<MetadataResponse>('/metadata');
    return res.data;
  },

  async getDatasets(): Promise<DatasetListResponse> {
    const client = createApiClient();
    const res = await client.get<DatasetListResponse>('/datasets');
    return res.data;
  },

  async runInvestigation(payload: InvestigationRequest): Promise<InvestigationResponse> {
    const client = createApiClient();
    const res = await client.post<InvestigationResponse>('/investigate', payload);
    return res.data;
  },

  async runQuery(payload: QueryRequest): Promise<QueryResponse> {
    const client = createApiClient();
    const res = await client.post<QueryResponse>('/query', payload);
    return res.data;
  },

  async getReport(id: string, format: 'json' | 'markdown' = 'json'): Promise<ReportResponse | string> {
    const client = createApiClient();
    if (format === 'markdown') {
      const res = await client.get<string>(`/report/${id}`, {
        headers: { Accept: 'text/markdown' },
        responseType: 'text',
      });
      return res.data;
    }
    const res = await client.get<ReportResponse>(`/report/${id}`);
    return res.data;
  },

  async getGraph(id: string): Promise<GraphResponse> {
    const client = createApiClient();
    const res = await client.get<GraphResponse>(`/graph/${id}`);
    return res.data;
  },

  async getVerdict(id: string): Promise<VerdictResponse> {
    const client = createApiClient();
    const res = await client.get<VerdictResponse>(`/verdict/${id}`);
    return res.data;
  },

  async listInvestigations(limit = 50, offset = 0): Promise<InvestigationListResponse> {
    const client = createApiClient();
    const res = await client.get<InvestigationListResponse>('/investigations', {
      params: { limit, offset },
    });
    return res.data;
  },

  async getInvestigationDetail(id: string): Promise<InvestigationDetailResponse> {
    const client = createApiClient();
    const res = await client.get<InvestigationDetailResponse>(`/investigation/${id}`);
    return res.data;
  },

  async deleteInvestigation(id: string): Promise<void> {
    const client = createApiClient();
    await client.delete(`/investigation/${id}`);
  },
};
