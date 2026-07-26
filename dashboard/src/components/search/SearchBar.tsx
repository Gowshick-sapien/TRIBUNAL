import React from 'react';
import { Search, X, SlidersHorizontal } from 'lucide-react';

interface SearchBarProps {
  value: string;
  onChange: (val: string) => void;
  onToggleFilters: () => void;
  showFilters: boolean;
}

export const SearchBar: React.FC<SearchBarProps> = ({
  value,
  onChange,
  onToggleFilters,
  showFilters,
}) => {
  return (
    <div className="flex flex-col sm:flex-row gap-3 items-center w-full">
      <div className="relative flex-1 w-full">
        <Search className="w-5 h-5 text-slate-500 absolute left-3.5 top-3 pointer-events-none" />
        <input
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder="Search by Case ID, Query, Hypothesis, Intent, or Recommendation..."
          className="w-full bg-slate-900/90 border border-slate-700 focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 rounded-xl py-2.5 pl-11 pr-10 text-sm text-slate-100 placeholder-slate-500 font-sans transition"
        />
        {value && (
          <button
            onClick={() => onChange('')}
            className="absolute right-3.5 top-3 text-slate-500 hover:text-slate-300 transition"
          >
            <X className="w-4 h-4" />
          </button>
        )}
      </div>

      <button
        onClick={onToggleFilters}
        className={`px-4 py-2.5 rounded-xl font-mono text-xs font-bold transition flex items-center gap-2 border ${
          showFilters
            ? 'bg-cyan-500 text-slate-950 border-cyan-400 shadow-lg shadow-cyan-500/20'
            : 'bg-slate-900 border-slate-700 text-slate-300 hover:bg-slate-800'
        }`}
      >
        <SlidersHorizontal className="w-4 h-4" />
        {showFilters ? 'Hide Filters' : 'Advanced Filters'}
      </button>
    </div>
  );
};
