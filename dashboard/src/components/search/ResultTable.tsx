import React from 'react';
import {
  Bookmark,
  Eye,
  Layers,
  FileText,
  CheckSquare,
  Square,
  ChevronLeft,
  ChevronRight,
  Download,
} from 'lucide-react';
import type { SearchResultItem } from '../../types/search';
import { RiskChip } from '../common/RiskChip';

interface ResultTableProps {
  items: SearchResultItem[];
  total: number;
  limit: number;
  offset: number;
  loading: boolean;
  selectedForCompare: string[];
  onToggleCompare: (id: string) => void;
  onToggleBookmark: (id: string) => void;
  onPreview: (item: SearchResultItem) => void;
  onNavigateViewer: (id: string) => void;
  onNavigateGraph: (id: string) => void;
  onPageChange: (newOffset: number) => void;
  onExport: (format: 'csv' | 'json') => void;
}

export const ResultTable: React.FC<ResultTableProps> = ({
  items,
  total,
  limit,
  offset,
  loading,
  selectedForCompare,
  onToggleCompare,
  onToggleBookmark,
  onPreview,
  onNavigateViewer,
  onNavigateGraph,
  onPageChange,
  onExport,
}) => {
  const currentPage = Math.floor(offset / limit) + 1;
  const totalPages = Math.ceil(total / limit) || 1;

  if (loading) {
    return (
      <div className="surface-card p-12 rounded-lg border border-slate-200 text-center font-sans text-xs text-slate-500 flex flex-col items-center gap-3">
        <span className="w-5 h-5 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />
        Searching repository metadata...
      </div>
    );
  }

  if (items.length === 0) {
    return (
      <div className="surface-card p-12 rounded-lg border border-slate-200 text-center font-sans text-xs text-slate-500 space-y-2">
        <p className="text-slate-900 font-semibold">No matching investigations found.</p>
        <p>Try adjusting your search criteria, clearing filters, or choosing a different dataset.</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Table Export Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 font-sans text-xs text-slate-500 border-b border-slate-200 pb-3">
        <div>
          Found <span className="text-slate-900 font-semibold">{total}</span> matching investigation(s) in repository
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => onExport('csv')}
            className="px-3 py-1.5 rounded-md bg-white hover:bg-slate-50 border border-slate-200 text-slate-700 transition-colors flex items-center gap-1.5 text-xs font-medium shadow-xs"
          >
            <Download className="w-3.5 h-3.5" /> Export CSV
          </button>
          <button
            onClick={() => onExport('json')}
            className="px-3 py-1.5 rounded-md bg-white hover:bg-slate-50 border border-slate-200 text-slate-700 transition-colors flex items-center gap-1.5 text-xs font-medium shadow-xs"
          >
            <Download className="w-3.5 h-3.5" /> Export JSON
          </button>
        </div>
      </div>

      {/* Main Table */}
      <div className="surface-card rounded-lg border border-slate-200 overflow-x-auto">
        <table className="w-full text-left font-sans text-xs">
          <thead className="bg-slate-50 border-b border-slate-200 text-slate-500 uppercase text-[10px] tracking-wider font-semibold">
            <tr>
              <th className="p-3 w-10 text-center">Compare</th>
              <th className="p-3 w-10 text-center">Bookmark</th>
              <th className="p-3">Investigation ID</th>
              <th className="p-3">Risk</th>
              <th className="p-3">Confidence</th>
              <th className="p-3">Target Query</th>
              <th className="p-3">Winning Hypothesis</th>
              <th className="p-3">Dataset</th>
              <th className="p-3 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {items.map((item) => {
              const isComparing = selectedForCompare.includes(item.id);
              return (
                <tr key={item.id} className="hover:bg-slate-50/80 transition-colors">
                  {/* Compare Selection Checkbox */}
                  <td className="p-3 text-center">
                    <button
                      onClick={() => onToggleCompare(item.id)}
                      className="text-slate-400 hover:text-blue-600 transition-colors"
                      title="Select for Side-by-Side Comparison"
                    >
                      {isComparing ? (
                        <CheckSquare className="w-4 h-4 text-blue-600" />
                      ) : (
                        <Square className="w-4 h-4" />
                      )}
                    </button>
                  </td>

                  {/* Bookmark Button */}
                  <td className="p-3 text-center">
                    <button
                      onClick={() => onToggleBookmark(item.id)}
                      className="text-slate-400 hover:text-amber-500 transition-colors"
                      title="Bookmark Investigation"
                    >
                      <Bookmark
                        className={`w-4 h-4 ${
                          item.is_bookmarked ? 'fill-amber-500 text-amber-500' : ''
                        }`}
                      />
                    </button>
                  </td>

                  {/* ID */}
                  <td className="p-3">
                    <span className="font-mono font-semibold text-blue-600">{item.id}</span>
                    <span className="block text-[10px] text-slate-400 font-sans">
                      {new Date(item.created_at).toLocaleDateString()}
                    </span>
                  </td>

                  {/* Risk */}
                  <td className="p-3">
                    <RiskChip risk={item.risk_level} />
                  </td>

                  {/* Confidence */}
                  <td className="p-3 font-mono font-semibold text-slate-900">
                    {(item.confidence * 100).toFixed(0)}%
                  </td>

                  {/* Query */}
                  <td className="p-3 max-w-xs truncate text-slate-900 font-medium" title={item.query}>
                    {item.query}
                  </td>

                  {/* Winning Hypothesis */}
                  <td className="p-3 max-w-xs truncate text-slate-600">
                    {item.winning_hypothesis || 'Structuring / Velocity Anomaly'}
                  </td>

                  {/* Dataset */}
                  <td className="p-3 font-mono text-[11px] text-slate-500">{item.dataset}</td>

                  {/* Actions */}
                  <td className="p-3 text-right space-x-1">
                    <button
                      onClick={() => onPreview(item)}
                      className="p-1.5 rounded-md bg-white border border-slate-200 text-slate-600 hover:text-slate-900 hover:bg-slate-50 transition-colors shadow-xs"
                      title="Quick Preview Drawer"
                    >
                      <Eye className="w-3.5 h-3.5" />
                    </button>
                    <button
                      onClick={() => onNavigateViewer(item.id)}
                      className="p-1.5 rounded-md bg-white border border-slate-200 text-slate-600 hover:text-slate-900 hover:bg-slate-50 transition-colors shadow-xs"
                      title="Open Full Investigation Viewer"
                    >
                      <FileText className="w-3.5 h-3.5" />
                    </button>
                    <button
                      onClick={() => onNavigateGraph(item.id)}
                      className="p-1.5 rounded-md bg-white border border-slate-200 text-slate-600 hover:text-slate-900 hover:bg-slate-50 transition-colors shadow-xs"
                      title="Open Interactive Evidence Graph Studio"
                    >
                      <Layers className="w-3.5 h-3.5" />
                    </button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Pagination Footer */}
      <div className="flex items-center justify-between font-sans text-xs text-slate-500 pt-2">
        <div>
          Page <span className="text-slate-900 font-semibold font-mono">{currentPage}</span> of{' '}
          <span className="text-slate-900 font-semibold font-mono">{totalPages}</span>
        </div>
        <div className="flex items-center gap-2">
          <button
            disabled={offset === 0}
            onClick={() => onPageChange(Math.max(0, offset - limit))}
            className="px-3 py-1.5 rounded-md bg-white hover:bg-slate-50 border border-slate-200 text-slate-700 transition-colors disabled:opacity-40 flex items-center gap-1 font-medium shadow-xs"
          >
            <ChevronLeft className="w-3.5 h-3.5" /> Prev
          </button>
          <button
            disabled={offset + limit >= total}
            onClick={() => onPageChange(offset + limit)}
            className="px-3 py-1.5 rounded-md bg-white hover:bg-slate-50 border border-slate-200 text-slate-700 transition-colors disabled:opacity-40 flex items-center gap-1 font-medium shadow-xs"
          >
            Next <ChevronRight className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
    </div>
  );
};
