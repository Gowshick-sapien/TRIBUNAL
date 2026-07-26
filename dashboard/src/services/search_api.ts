import axios from 'axios';
import { getApiBaseUrl } from './api';
import type {
  SearchFilterState,
  SearchResponse,
  SearchResultItem,
  SimilarListResponse,
} from '../types/search';

const createClient = () => {
  return axios.create({
    baseURL: getApiBaseUrl(),
    headers: { 'Content-Type': 'application/json' },
    timeout: 30000,
  });
};

export const searchApi = {
  async search(filters: SearchFilterState, limit = 20, offset = 0): Promise<SearchResponse> {
    const client = createClient();
    const params: Record<string, any> = {
      limit,
      offset,
      sort_by: filters.sort_by,
    };

    if (filters.query && filters.query.trim()) params.query = filters.query.trim();
    if (filters.risk_level && filters.risk_level !== 'ALL') params.risk_level = filters.risk_level;
    if (filters.min_confidence > 0) params.min_confidence = filters.min_confidence;
    if (filters.max_confidence < 1.0) params.max_confidence = filters.max_confidence;
    if (filters.dataset && filters.dataset !== 'ALL') params.dataset = filters.dataset;
    if (filters.status && filters.status !== 'ALL') params.status = filters.status;
    if (filters.only_bookmarked) params.only_bookmarked = true;

    const res = await client.get<SearchResponse>('/search', { params });
    return res.data;
  },

  async getRecent(limit = 10): Promise<SearchResultItem[]> {
    const client = createClient();
    const res = await client.get<SearchResultItem[]>('/search/recent', { params: { limit } });
    return res.data;
  },

  async getBookmarks(): Promise<SearchResultItem[]> {
    const client = createClient();
    const res = await client.get<SearchResultItem[]>('/search/bookmarks');
    return res.data;
  },

  async toggleBookmark(id: string): Promise<boolean> {
    const client = createClient();
    const res = await client.post<{ is_bookmarked: boolean }>(`/search/bookmarks/${id}`);
    return res.data.is_bookmarked;
  },

  async getSimilar(id: string, limit = 5): Promise<SimilarListResponse> {
    const client = createClient();
    const res = await client.get<SimilarListResponse>(`/search/similar/${id}`, { params: { limit } });
    return res.data;
  },

  async addTag(id: string, tag: string): Promise<void> {
    const client = createClient();
    await client.post(`/search/tags/${id}`, { tag });
  },

  async removeTag(id: string, tag: string): Promise<void> {
    const client = createClient();
    await client.delete(`/search/tags/${id}`, { params: { tag } });
  },

  getExportUrl(filters: SearchFilterState, format: 'csv' | 'json' = 'csv'): string {
    const base = getApiBaseUrl();
    const q = encodeURIComponent(filters.query || '');
    return `${base}/search/export?query=${q}&risk_level=${filters.risk_level}&format=${format}`;
  },
};
