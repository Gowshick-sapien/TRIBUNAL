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
        <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3 pointer-events-none" />
        <input
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder="Search by Case ID, Query, Hypothesis, Intent, or Recommendation..."
          className="w-full bg-white border border-slate-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 rounded-md py-2 pl-10 pr-10 text-sm text-slate-900 placeholder-slate-400 font-sans shadow-xs transition-colors"
        />
        {value && (
          <button
            onClick={() => onChange('')}
            className="absolute right-3.5 top-2.5 text-slate-400 hover:text-slate-600 transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        )}
      </div>

      <button
        onClick={onToggleFilters}
        className={`px-3.5 py-2 rounded-md font-sans text-xs font-medium transition-colors flex items-center gap-2 border shadow-xs ${
          showFilters
            ? 'bg-blue-600 text-white border-blue-600'
            : 'bg-white border-slate-200 text-slate-700 hover:bg-slate-50 hover:text-slate-900'
        }`}
      >
        <SlidersHorizontal className="w-3.5 h-3.5" />
        {showFilters ? 'Hide Filters' : 'Advanced Filters'}
      </button>
    </div>
  );
};
