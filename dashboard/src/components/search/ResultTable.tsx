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
      <div className="glass-panel p-12 rounded-2xl border border-slate-800 text-center font-mono text-xs text-slate-500 flex flex-col items-center gap-3">
        <span className="w-6 h-6 border-2 border-cyan-400 border-t-transparent rounded-full animate-spin" />
        Searching repository metadata...
      </div>
    );
  }

  if (items.length === 0) {
    return (
      <div className="glass-panel p-12 rounded-2xl border border-slate-800 text-center font-mono text-xs text-slate-500 space-y-2">
        <p className="text-slate-300 font-bold">No matching investigations found.</p>
        <p>Try adjusting your search criteria, clearing filters, or choosing a different dataset.</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Table Export Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 font-mono text-xs text-slate-400 border-b border-slate-800 pb-3">
        <div>
          Found <span className="text-cyan-400 font-bold">{total}</span> matching investigation(s) in repository
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => onExport('csv')}
            className="px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-200 transition flex items-center gap-1.5 text-xs font-bold"
          >
            <Download className="w-3.5 h-3.5" /> Export CSV
          </button>
          <button
            onClick={() => onExport('json')}
            className="px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-200 transition flex items-center gap-1.5 text-xs font-bold"
          >
            <Download className="w-3.5 h-3.5" /> Export JSON
          </button>
        </div>
      </div>

      {/* Main Table */}
      <div className="glass-panel rounded-2xl border border-slate-800 overflow-x-auto">
        <table className="w-full text-left font-mono text-xs">
          <thead className="bg-slate-900/80 border-b border-slate-800 text-slate-400 uppercase text-[10px] tracking-wider">
            <tr>
              <th className="p-3.5 w-10 text-center">Compare</th>
              <th className="p-3.5 w-10 text-center">Bookmark</th>
              <th className="p-3.5">Investigation ID</th>
              <th className="p-3.5">Risk</th>
              <th className="p-3.5">Confidence</th>
              <th className="p-3.5">Target Query</th>
              <th className="p-3.5">Winning Hypothesis</th>
              <th className="p-3.5">Dataset</th>
              <th className="p-3.5 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/80">
            {items.map((item) => {
              const isComparing = selectedForCompare.includes(item.id);
              return (
                <tr key={item.id} className="hover:bg-slate-900/40 transition">
                  {/* Compare Selection Checkbox */}
                  <td className="p-3.5 text-center">
                    <button
                      onClick={() => onToggleCompare(item.id)}
                      className="text-slate-500 hover:text-cyan-400 transition"
                      title="Select for Side-by-Side Comparison"
                    >
                      {isComparing ? (
                        <CheckSquare className="w-4 h-4 text-cyan-400" />
                      ) : (
                        <Square className="w-4 h-4" />
                      )}
                    </button>
                  </td>

                  {/* Bookmark Button */}
                  <td className="p-3.5 text-center">
                    <button
                      onClick={() => onToggleBookmark(item.id)}
                      className="text-slate-500 hover:text-amber-400 transition"
                      title="Bookmark Investigation"
                    >
                      <Bookmark
                        className={`w-4 h-4 ${
                          item.is_bookmarked ? 'fill-amber-400 text-amber-400' : ''
                        }`}
                      />
                    </button>
                  </td>

                  {/* ID */}
                  <td className="p-3.5">
                    <span className="font-bold text-cyan-400">{item.id}</span>
                    <span className="block text-[10px] text-slate-500">
                      {new Date(item.created_at).toLocaleDateString()}
                    </span>
                  </td>

                  {/* Risk */}
                  <td className="p-3.5">
                    <RiskChip risk={item.risk_level} />
                  </td>

                  {/* Confidence */}
                  <td className="p-3.5 font-bold text-slate-200">
                    {(item.confidence * 100).toFixed(0)}%
                  </td>

                  {/* Query */}
                  <td className="p-3.5 max-w-xs truncate font-sans text-slate-200" title={item.query}>
                    {item.query}
                  </td>

                  {/* Winning Hypothesis */}
                  <td className="p-3.5 max-w-xs truncate font-sans text-slate-300">
                    {item.winning_hypothesis || 'Structuring / Velocity Anomaly'}
                  </td>

                  {/* Dataset */}
                  <td className="p-3.5 font-mono text-[11px] text-slate-400">{item.dataset}</td>

                  {/* Actions */}
                  <td className="p-3.5 text-right space-x-1">
                    <button
                      onClick={() => onPreview(item)}
                      className="p-1.5 rounded bg-slate-900 hover:bg-slate-800 text-slate-300 hover:text-cyan-400 transition"
                      title="Quick Preview Drawer"
                    >
                      <Eye className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => onNavigateViewer(item.id)}
                      className="p-1.5 rounded bg-slate-900 hover:bg-slate-800 text-slate-300 hover:text-cyan-400 transition"
                      title="Open Full Investigation Viewer"
                    >
                      <FileText className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => onNavigateGraph(item.id)}
                      className="p-1.5 rounded bg-slate-900 hover:bg-slate-800 text-slate-300 hover:text-cyan-400 transition"
                      title="Open Interactive Evidence Graph Studio"
                    >
                      <Layers className="w-4 h-4" />
                    </button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Pagination Footer */}
      <div className="flex items-center justify-between font-mono text-xs text-slate-400 pt-2">
        <div>
          Page <span className="text-cyan-400 font-bold">{currentPage}</span> of{' '}
          <span className="text-slate-200 font-bold">{totalPages}</span>
        </div>
        <div className="flex items-center gap-2">
          <button
            disabled={offset === 0}
            onClick={() => onPageChange(Math.max(0, offset - limit))}
            className="px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 transition disabled:opacity-40 flex items-center gap-1"
          >
            <ChevronLeft className="w-4 h-4" /> Prev
          </button>
          <button
            disabled={offset + limit >= total}
            onClick={() => onPageChange(offset + limit)}
            className="px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 transition disabled:opacity-40 flex items-center gap-1"
          >
            Next <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};
