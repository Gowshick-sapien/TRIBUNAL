import React from 'react';
import { Bookmark, RotateCcw } from 'lucide-react';
import type { SearchFilterState } from '../../types/search';

interface FilterPanelProps {
  filters: SearchFilterState;
  onChange: (newFilters: SearchFilterState) => void;
  onReset: () => void;
}

export const FilterPanel: React.FC<FilterPanelProps> = ({
  filters,
  onChange,
  onReset,
}) => {
  return (
    <div className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-4 animate-fadeIn font-mono text-xs">
      <div className="flex items-center justify-between border-b border-slate-800 pb-2">
        <span className="font-bold text-slate-300 uppercase tracking-wider text-[11px]">
          Multi-Criteria Repository Filters
        </span>
        <button
          onClick={onReset}
          className="text-slate-400 hover:text-cyan-400 transition flex items-center gap-1 text-[11px]"
        >
          <RotateCcw className="w-3 h-3" /> Reset
        </button>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
        {/* Risk Filter */}
        <div className="space-y-1.5">
          <label className="text-[10px] text-slate-400 uppercase font-bold">Risk Classification</label>
          <select
            value={filters.risk_level}
            onChange={(e) => onChange({ ...filters, risk_level: e.target.value })}
            className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-slate-200"
          >
            <option value="ALL">ALL RISKS</option>
            <option value="CRITICAL">CRITICAL</option>
            <option value="HIGH">HIGH</option>
            <option value="MEDIUM">MEDIUM</option>
            <option value="LOW">LOW</option>
          </select>
        </div>

        {/* Dataset Alias Filter */}
        <div className="space-y-1.5">
          <label className="text-[10px] text-slate-400 uppercase font-bold">Dataset Reference</label>
          <select
            value={filters.dataset}
            onChange={(e) => onChange({ ...filters, dataset: e.target.value })}
            className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-slate-200"
          >
            <option value="ALL">ALL DATASETS</option>
            <option value="default">Default Dataset</option>
            <option value="li_small">IBM AML Small CSV</option>
            <option value="ibm_small">IBM Transactions Parquet</option>
            <option value="synthetic">Synthetic AML Demo</option>
          </select>
        </div>

        {/* Status Filter */}
        <div className="space-y-1.5">
          <label className="text-[10px] text-slate-400 uppercase font-bold">Status</label>
          <select
            value={filters.status}
            onChange={(e) => onChange({ ...filters, status: e.target.value })}
            className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-slate-200"
          >
            <option value="ALL">ALL STATUSES</option>
            <option value="COMPLETED">COMPLETED</option>
            <option value="FAILED">FAILED</option>
          </select>
        </div>

        {/* Sort By */}
        <div className="space-y-1.5">
          <label className="text-[10px] text-slate-400 uppercase font-bold">Sort Order</label>
          <select
            value={filters.sort_by}
            onChange={(e) => onChange({ ...filters, sort_by: e.target.value })}
            className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-slate-200 font-bold text-cyan-400"
          >
            <option value="newest">Newest First</option>
            <option value="oldest">Oldest First</option>
            <option value="confidence_desc">Highest Confidence</option>
            <option value="risk_desc">Highest Risk Level</option>
            <option value="fastest">Fastest Execution</option>
          </select>
        </div>
      </div>

      {/* Confidence Range Slider & Bookmarks Checkbox */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2 border-t border-slate-800/80 items-center">
        <div className="space-y-1">
          <div className="flex justify-between text-[10px] text-slate-400 uppercase font-bold">
            <span>Min Confidence Threshold</span>
            <span className="text-cyan-400 font-bold">{(filters.min_confidence * 100).toFixed(0)}%</span>
          </div>
          <input
            type="range"
            min="0"
            max="1"
            step="0.05"
            value={filters.min_confidence}
            onChange={(e) => onChange({ ...filters, min_confidence: parseFloat(e.target.value) })}
            className="w-full accent-cyan-400 bg-slate-800"
          />
        </div>

        <div className="flex items-center gap-2 pt-2 md:pt-0">
          <button
            type="button"
            onClick={() => onChange({ ...filters, only_bookmarked: !filters.only_bookmarked })}
            className={`px-3 py-2 rounded-lg font-bold text-xs transition flex items-center gap-1.5 border ${
              filters.only_bookmarked
                ? 'bg-amber-500 text-slate-950 border-amber-400'
                : 'bg-slate-900 border-slate-700 text-slate-300 hover:bg-slate-800'
            }`}
          >
            <Bookmark className="w-3.5 h-3.5" />
            {filters.only_bookmarked ? 'Bookmarked Items Only' : 'Filter Bookmarks Only'}
          </button>
        </div>
      </div>
    </div>
  );
};
