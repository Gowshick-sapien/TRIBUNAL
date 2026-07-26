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
    <div className="surface-card p-5 rounded-lg border border-slate-200 space-y-4 font-sans text-xs">
      <div className="flex items-center justify-between border-b border-slate-200 pb-2.5">
        <span className="font-semibold text-slate-900 uppercase tracking-wider text-[10px]">
          Multi-Criteria Repository Filters
        </span>
        <button
          onClick={onReset}
          className="text-slate-500 hover:text-slate-900 transition-colors flex items-center gap-1 text-xs font-medium"
        >
          <RotateCcw className="w-3.5 h-3.5" /> Reset Filters
        </button>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
        {/* Risk Filter */}
        <div className="space-y-1.5">
          <label className="text-[10px] text-slate-500 uppercase font-semibold">Risk Classification</label>
          <select
            value={filters.risk_level}
            onChange={(e) => onChange({ ...filters, risk_level: e.target.value })}
            className="w-full bg-white border border-slate-200 rounded-md p-2 text-slate-900 font-sans"
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
          <label className="text-[10px] text-slate-500 uppercase font-semibold">Dataset Reference</label>
          <select
            value={filters.dataset}
            onChange={(e) => onChange({ ...filters, dataset: e.target.value })}
            className="w-full bg-white border border-slate-200 rounded-md p-2 text-slate-900 font-sans"
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
          <label className="text-[10px] text-slate-500 uppercase font-semibold">Status</label>
          <select
            value={filters.status}
            onChange={(e) => onChange({ ...filters, status: e.target.value })}
            className="w-full bg-white border border-slate-200 rounded-md p-2 text-slate-900 font-sans"
          >
            <option value="ALL">ALL STATUSES</option>
            <option value="COMPLETED">COMPLETED</option>
            <option value="FAILED">FAILED</option>
          </select>
        </div>

        {/* Sort By */}
        <div className="space-y-1.5">
          <label className="text-[10px] text-slate-500 uppercase font-semibold">Sort Order</label>
          <select
            value={filters.sort_by}
            onChange={(e) => onChange({ ...filters, sort_by: e.target.value })}
            className="w-full bg-white border border-slate-200 rounded-md p-2 text-slate-900 font-sans font-medium"
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
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-3 border-t border-slate-200 items-center">
        <div className="space-y-1">
          <div className="flex justify-between text-[10px] text-slate-500 uppercase font-semibold">
            <span>Min Confidence Threshold</span>
            <span className="text-blue-600 font-mono font-semibold">{(filters.min_confidence * 100).toFixed(0)}%</span>
          </div>
          <input
            type="range"
            min="0"
            max="1"
            step="0.05"
            value={filters.min_confidence}
            onChange={(e) => onChange({ ...filters, min_confidence: parseFloat(e.target.value) })}
            className="w-full accent-blue-600 bg-slate-200 h-1.5 rounded-md"
          />
        </div>

        <div className="flex items-center gap-2 pt-2 md:pt-0">
          <button
            type="button"
            onClick={() => onChange({ ...filters, only_bookmarked: !filters.only_bookmarked })}
            className={`px-3 py-1.5 rounded-md font-sans text-xs font-medium transition-colors flex items-center gap-1.5 border shadow-xs ${
              filters.only_bookmarked
                ? 'bg-amber-50 text-amber-700 border-amber-200'
                : 'bg-white border-slate-200 text-slate-700 hover:bg-slate-50'
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
