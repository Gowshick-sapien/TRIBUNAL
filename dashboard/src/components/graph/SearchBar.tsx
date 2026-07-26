import React from 'react';
import { Search, Filter, X } from 'lucide-react';
import type { GraphFilterOptions } from '../../types/graph';

interface SearchBarProps {
  filters: GraphFilterOptions;
  onChange: (newFilters: GraphFilterOptions) => void;
}

export const SearchBar: React.FC<SearchBarProps> = ({ filters, onChange }) => {
  return (
    <div className="glass-panel p-3 rounded-xl border border-slate-800 flex flex-wrap items-center gap-3 shadow-lg font-mono text-xs">
      {/* Search Input */}
      <div className="relative flex-1 min-w-[200px]">
        <Search className="w-4 h-4 text-slate-500 absolute left-3 top-2.5 pointer-events-none" />
        <input
          type="text"
          value={filters.searchQuery}
          onChange={(e) => onChange({ ...filters, searchQuery: e.target.value })}
          placeholder="Search by Card ID, Hypothesis, Expert, or TX..."
          className="w-full bg-slate-900 border border-slate-700 focus:border-cyan-500 rounded-lg py-1.5 pl-9 pr-8 text-xs text-slate-200 placeholder-slate-500"
        />
        {filters.searchQuery && (
          <button
            onClick={() => onChange({ ...filters, searchQuery: '' })}
            className="absolute right-2.5 top-2.5 text-slate-500 hover:text-slate-300"
          >
            <X className="w-3.5 h-3.5" />
          </button>
        )}
      </div>

      {/* Expert Filter */}
      <div className="flex items-center gap-1.5">
        <Filter className="w-3.5 h-3.5 text-slate-500" />
        <span className="text-slate-400 text-[11px]">Expert:</span>
        <select
          value={filters.expertFilter}
          onChange={(e) => onChange({ ...filters, expertFilter: e.target.value })}
          className="bg-slate-900 border border-slate-700 focus:border-cyan-500 rounded-lg py-1.5 px-2 text-xs text-slate-200"
        >
          <option value="ALL">ALL EXPERTS</option>
          <option value="financial">Financial Expert</option>
          <option value="behaviour">Behaviour Expert</option>
          <option value="defense">Defense Review</option>
        </select>
      </div>

      {/* Severity Filter */}
      <div className="flex items-center gap-1.5">
        <span className="text-slate-400 text-[11px]">Severity:</span>
        <select
          value={filters.severityFilter}
          onChange={(e) => onChange({ ...filters, severityFilter: e.target.value })}
          className="bg-slate-900 border border-slate-700 focus:border-cyan-500 rounded-lg py-1.5 px-2 text-xs text-slate-200"
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
