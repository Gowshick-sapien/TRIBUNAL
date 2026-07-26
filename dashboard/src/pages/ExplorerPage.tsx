import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { Database, ArrowLeftRight } from 'lucide-react';
import { searchApi } from '../services/search_api';
import type { SearchFilterState, SearchResultItem } from '../types/search';
import { SearchBar } from '../components/search/SearchBar';
import { FilterPanel } from '../components/search/FilterPanel';
import { ResultTable } from '../components/search/ResultTable';
import { InvestigationPreview } from '../components/search/InvestigationPreview';
import { SavedSearches } from '../components/search/SavedSearches';

export const ExplorerPage: React.FC = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  const [filters, setFilters] = useState<SearchFilterState>({
    query: searchParams.get('q') || '',
    risk_level: searchParams.get('risk') || 'ALL',
    min_confidence: parseFloat(searchParams.get('min_conf') || '0.0'),
    max_confidence: 1.0,
    dataset: searchParams.get('dataset') || 'ALL',
    status: 'ALL',
    only_bookmarked: searchParams.get('bookmarked') === 'true',
    sort_by: searchParams.get('sort') || 'newest',
  });

  const [showFilters, setShowFilters] = useState(false);
  const [items, setItems] = useState<SearchResultItem[]>([]);
  const [total, setTotal] = useState(0);
  const [limit] = useState(20);
  const [offset, setOffset] = useState(0);
  const [loading, setLoading] = useState(true);

  // Preview & Comparison selection state
  const [previewItem, setPreviewItem] = useState<SearchResultItem | null>(null);
  const [selectedForCompare, setSelectedForCompare] = useState<string[]>([]);

  const fetchResults = useCallback(async () => {
    setLoading(true);
    try {
      const data = await searchApi.search(filters, limit, offset);
      setItems(data.results);
      setTotal(data.total);
    } catch (err) {
      console.error('Search failed:', err);
    } finally {
      setLoading(false);
    }
  }, [filters, limit, offset]);

  useEffect(() => {
    fetchResults();
  }, [fetchResults]);

  const handleToggleBookmark = async (id: string) => {
    const isNowBookmarked = await searchApi.toggleBookmark(id);
    setItems((prev) =>
      prev.map((item) => (item.id === id ? { ...item, is_bookmarked: isNowBookmarked } : item))
    );
  };

  const handleToggleCompare = (id: string) => {
    setSelectedForCompare((prev) => {
      if (prev.includes(id)) {
        return prev.filter((item) => item !== id);
      }
      if (prev.length >= 2) {
        return [prev[1], id];
      }
      return [...prev, id];
    });
  };

  const handleExport = (format: 'csv' | 'json') => {
    const url = searchApi.getExportUrl(filters, format);
    window.open(url, '_blank');
  };

  const handleResetFilters = () => {
    setFilters({
      query: '',
      risk_level: 'ALL',
      min_confidence: 0.0,
      max_confidence: 1.0,
      dataset: 'ALL',
      status: 'ALL',
      only_bookmarked: false,
      sort_by: 'newest',
    });
    setOffset(0);
  };

  return (
    <div className="p-6 md:p-8 max-w-7xl mx-auto space-y-6 font-sans">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 pb-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 font-sans tracking-tight flex items-center gap-2">
            <Database className="w-5 h-5 text-blue-600" />
            Repository Explorer & Advanced Search Platform
          </h1>
          <p className="text-xs font-sans text-slate-500 mt-1">
            Discover, filter, rank by similarity, compare, bookmark, and export historical investigation metadata (Phase D.5).
          </p>
        </div>

        {/* Compare Action Button */}
        {selectedForCompare.length > 0 && (
          <button
            onClick={() =>
              navigate(`/compare?left=${selectedForCompare[0]}&right=${selectedForCompare[1] || ''}`)
            }
            className="px-4 py-2 rounded-md bg-blue-600 hover:bg-blue-700 text-white font-medium text-xs shadow-xs flex items-center gap-2 transition-colors shrink-0"
          >
            <ArrowLeftRight className="w-4 h-4" />
            Compare Selected ({selectedForCompare.length}/2) &rarr;
          </button>
        )}
      </div>

      {/* Search Bar */}
      <SearchBar
        value={filters.query}
        onChange={(val) => {
          setFilters({ ...filters, query: val });
          setOffset(0);
        }}
        onToggleFilters={() => setShowFilters(!showFilters)}
        showFilters={showFilters}
      />

      {/* Saved Search Presets */}
      <SavedSearches
        onApplyPreset={(preset) => {
          setFilters({ ...filters, ...preset });
          setOffset(0);
        }}
      />

      {/* Collapsible Filter Panel */}
      {showFilters && (
        <FilterPanel
          filters={filters}
          onChange={(newFilters) => {
            setFilters(newFilters);
            setOffset(0);
          }}
          onReset={handleResetFilters}
        />
      )}

      {/* Main Results Table */}
      <ResultTable
        items={items}
        total={total}
        limit={limit}
        offset={offset}
        loading={loading}
        selectedForCompare={selectedForCompare}
        onToggleCompare={handleToggleCompare}
        onToggleBookmark={handleToggleBookmark}
        onPreview={(item) => setPreviewItem(item)}
        onNavigateViewer={(id) => navigate(`/investigation/${id}`)}
        onNavigateGraph={(id) => navigate(`/graph/${id}`)}
        onPageChange={(newOffset) => setOffset(newOffset)}
        onExport={handleExport}
      />

      {/* Slide-Over Investigation Preview Drawer */}
      <InvestigationPreview
        item={previewItem}
        onClose={() => setPreviewItem(null)}
        onNavigateViewer={(id) => navigate(`/investigation/${id}`)}
        onNavigateGraph={(id) => navigate(`/graph/${id}`)}
      />
    </div>
  );
};
