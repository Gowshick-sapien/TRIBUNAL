import React from 'react';
import { Sparkles } from 'lucide-react';
import type { SearchFilterState } from '../../types/search';

interface SavedSearchesProps {
  onApplyPreset: (preset: Partial<SearchFilterState>) => void;
}

export const SavedSearches: React.FC<SavedSearchesProps> = ({ onApplyPreset }) => {
  const presets = [
    {
      label: 'CRITICAL Risk Cases',
      filters: { risk_level: 'CRITICAL', min_confidence: 0.0, only_bookmarked: false },
      badge: 'CRITICAL',
    },
    {
      label: 'High Confidence (>80%)',
      filters: { min_confidence: 0.8, risk_level: 'ALL', only_bookmarked: false },
      badge: '>80%',
    },
    {
      label: 'Bookmarked Investigations',
      filters: { only_bookmarked: true, risk_level: 'ALL', min_confidence: 0.0 },
      badge: 'Saved',
    },
    {
      label: 'Structuring Anomalies',
      filters: { query: 'Structuring', risk_level: 'ALL', min_confidence: 0.0 },
      badge: 'AML',
    },
  ];

  return (
    <div className="flex flex-wrap items-center gap-2 text-xs font-sans">
      <span className="text-slate-500 font-semibold uppercase text-[10px] flex items-center gap-1">
        <Sparkles className="w-3.5 h-3.5 text-blue-600" /> Presets:
      </span>
      {presets.map((p, idx) => (
        <button
          key={idx}
          onClick={() => onApplyPreset(p.filters)}
          className="px-2.5 py-1 rounded-md bg-white hover:bg-slate-50 border border-slate-200 text-slate-700 transition-colors flex items-center gap-1.5 shadow-xs font-medium"
        >
          <span>{p.label}</span>
          <span className="text-[10px] px-1.5 py-0.2 rounded bg-slate-100 border border-slate-200 text-slate-600 font-mono font-medium">
            {p.badge}
          </span>
        </button>
      ))}
    </div>
  );
};
