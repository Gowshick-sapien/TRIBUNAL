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
    <div className="surface-card p-3 rounded-lg border border-slate-200 flex flex-col sm:flex-row items-center justify-between gap-3 font-sans text-xs shadow-xs no-print">
      {/* Search Input */}
      <div className="relative flex-1 w-full max-w-md">
        <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-2 pointer-events-none" />
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => onSearchChange(e.target.value)}
          placeholder="Search text, transaction IDs, or accounts in report..."
          className="w-full bg-white border border-slate-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 rounded-md py-1.5 pl-9 pr-8 text-slate-900 placeholder-slate-400 text-xs font-sans"
        />
        {searchTerm && (
          <button
            onClick={() => onSearchChange('')}
            className="absolute right-2.5 top-2 text-slate-400 hover:text-slate-600 transition-colors"
          >
            <X className="w-3.5 h-3.5" />
          </button>
        )}
      </div>

      {/* Toolbar Controls */}
      <div className="flex items-center gap-2 shrink-0">
        <button
          onClick={onPrint}
          className="px-3 py-1.5 rounded-md bg-white hover:bg-slate-50 border border-slate-200 text-slate-700 font-medium transition-colors flex items-center gap-1.5 shadow-xs"
        >
          <Printer className="w-3.5 h-3.5 text-slate-600" />
          Print / PDF
        </button>

        <button
          onClick={onToggleAnnotations}
          className={`px-3 py-1.5 rounded-md font-medium transition-colors flex items-center gap-1.5 border shadow-xs ${
            showAnnotations
              ? 'bg-amber-50 text-amber-700 border-amber-200'
              : 'bg-white border-slate-200 text-slate-700 hover:bg-slate-50'
          }`}
        >
          <MessageSquare className="w-3.5 h-3.5" />
          Notes ({annotationCount})
        </button>
      </div>
    </div>
  );
};
