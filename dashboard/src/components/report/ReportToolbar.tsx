import React from 'react';
import { Search, Printer, MessageSquare, X } from 'lucide-react';

interface ReportToolbarProps {
  searchTerm: string;
  onSearchChange: (val: string) => void;
  onPrint: () => void;
  onToggleAnnotations: () => void;
  showAnnotations: boolean;
  annotationCount: number;
}

export const ReportToolbar: React.FC<ReportToolbarProps> = ({
  searchTerm,
  onSearchChange,
  onPrint,
  onToggleAnnotations,
  showAnnotations,
  annotationCount,
}) => {
  return (
    <div className="glass-panel p-3.5 rounded-2xl border border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-3 font-mono text-xs no-print">
      {/* Search Input */}
      <div className="relative flex-1 w-full max-w-md">
        <Search className="w-4 h-4 text-slate-500 absolute left-3 top-2.5 pointer-events-none" />
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => onSearchChange(e.target.value)}
          placeholder="Search text, transaction IDs, or accounts in report..."
          className="w-full bg-slate-900 border border-slate-700 focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 rounded-xl py-1.5 pl-9 pr-8 text-slate-100 placeholder-slate-500 text-xs"
        />
        {searchTerm && (
          <button
            onClick={() => onSearchChange('')}
            className="absolute right-2.5 top-2.5 text-slate-500 hover:text-slate-300 transition"
          >
            <X className="w-3.5 h-3.5" />
          </button>
        )}
      </div>

      {/* Toolbar Controls */}
      <div className="flex items-center gap-2 shrink-0">
        <button
          onClick={onPrint}
          className="px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-200 font-bold transition flex items-center gap-1.5"
        >
          <Printer className="w-3.5 h-3.5 text-purple-400" />
          Print / PDF
        </button>

        <button
          onClick={onToggleAnnotations}
          className={`px-3 py-1.5 rounded-lg font-bold transition flex items-center gap-1.5 border ${
            showAnnotations
              ? 'bg-amber-500 text-slate-950 border-amber-400'
              : 'bg-slate-900 border-slate-700 text-slate-300 hover:bg-slate-800'
          }`}
        >
          <MessageSquare className="w-3.5 h-3.5" />
          Notes ({annotationCount})
        </button>
      </div>
    </div>
  );
};
