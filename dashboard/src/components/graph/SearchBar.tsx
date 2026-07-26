import React from 'react';
import { Search, Filter, X } from 'lucide-react';
import type { GraphFilterOptions } from '../../types/graph';

interface SearchBarProps {
  filters: GraphFilterOptions;
  onChange: (newFilters: GraphFilterOptions) => void;
}

export const SearchBar: React.FC<SearchBarProps> = ({ filters, onChange }) => {
  return (
    <div className="surface-card p-3 rounded-lg border border-slate-200 flex flex-wrap items-center gap-3 shadow-xs font-sans text-xs bg-white">
      {/* Search Input */}
      <div className="relative flex-1 min-w-[200px]">
        <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-2 pointer-events-none" />
        <input
          type="text"
          value={filters.searchQuery}
          onChange={(e) => onChange({ ...filters, searchQuery: e.target.value })}
          placeholder="Search by Card ID, Hypothesis, Expert, or TX..."
          className="w-full bg-white border border-slate-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 rounded-md py-1.5 pl-9 pr-8 text-xs text-slate-900 placeholder-slate-400 font-sans"
        />
        {filters.searchQuery && (
          <button
            onClick={() => onChange({ ...filters, searchQuery: '' })}
            className="absolute right-2.5 top-2 text-slate-400 hover:text-slate-600 transition-colors"
          >
            <X className="w-3.5 h-3.5" />
          </button>
        )}
      </div>

      {/* Expert Filter */}
      <div className="flex items-center gap-1.5">
        <Filter className="w-3.5 h-3.5 text-slate-400" />
        <span className="text-slate-500 text-[11px] font-medium">Expert:</span>
        <select
          value={filters.expertFilter}
          onChange={(e) => onChange({ ...filters, expertFilter: e.target.value })}
          className="bg-white border border-slate-200 focus:border-blue-500 rounded-md py-1.5 px-2 text-xs text-slate-900 font-sans"
        >
          <option value="ALL">ALL EXPERTS</option>
          <option value="financial">Financial Expert</option>
          <option value="behaviour">Behaviour Expert</option>
          <option value="defense">Defense Review</option>
        </select>
      </div>

      {/* Severity Filter */}
      <div className="flex items-center gap-1.5">
        <span className="text-slate-500 text-[11px] font-medium">Severity:</span>
        <select
          value={filters.severityFilter}
          onChange={(e) => onChange({ ...filters, severityFilter: e.target.value })}
          className="bg-white border border-slate-200 focus:border-blue-500 rounded-md py-1.5 px-2 text-xs text-slate-900 font-sans"
        >
          <option value="ALL">ALL SEVERITIES</option>
          <option value="CRITICAL">CRITICAL</option>
          <option value="HIGH">HIGH</option>
          <option value="MEDIUM">MEDIUM</option>
        </select>
      </div>
    </div>
  );
};
