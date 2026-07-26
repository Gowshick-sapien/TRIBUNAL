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
    <div className="flex flex-wrap items-center gap-2 text-xs font-mono">
      <span className="text-slate-500 font-bold uppercase text-[10px] flex items-center gap-1">
        <Sparkles className="w-3 h-3 text-cyan-400" /> Presets:
      </span>
      {presets.map((p, idx) => (
        <button
          key={idx}
          onClick={() => onApplyPreset(p.filters)}
          className="px-2.5 py-1 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 transition flex items-center gap-1.5"
        >
          <span>{p.label}</span>
          <span className="text-[9px] px-1 py-0.2 rounded bg-slate-950 text-cyan-400 font-bold">
            {p.badge}
          </span>
        </button>
      ))}
    </div>
  );
};
