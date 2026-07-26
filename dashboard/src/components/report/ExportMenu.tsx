import React, { useState } from 'react';
import { Download, Printer, FileText, Code, FileCode } from 'lucide-react';
import { reportApi } from '../../services/report_api';

interface ExportMenuProps {
  reportId: string;
  onPrint: () => void;
}

export const ExportMenu: React.FC<ExportMenuProps> = ({ reportId, onPrint }) => {
  const [open, setOpen] = useState(false);

  const handleDownload = (format: 'markdown' | 'html' | 'pdf' | 'json') => {
    const url = reportApi.getExportUrl(reportId, format);
    window.open(url, '_blank');
    setOpen(false);
  };

  return (
    <div className="relative">
      <button
        onClick={() => setOpen(!open)}
        className="px-3.5 py-2 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold font-mono text-xs transition flex items-center gap-1.5 shadow-md shadow-cyan-500/20"
      >
        <Download className="w-4 h-4" />
        Export Report
      </button>

      {open && (
        <div className="absolute right-0 mt-2 w-48 glass-panel border border-slate-700 rounded-xl p-1.5 shadow-2xl z-50 font-mono text-xs space-y-1">
          <button
            onClick={() => handleDownload('markdown')}
            className="w-full text-left px-3 py-2 rounded-lg hover:bg-slate-800 text-slate-200 transition flex items-center gap-2"
          >
            <FileText className="w-4 h-4 text-cyan-400" />
            Markdown (.md)
          </button>
          <button
            onClick={() => handleDownload('html')}
            className="w-full text-left px-3 py-2 rounded-lg hover:bg-slate-800 text-slate-200 transition flex items-center gap-2"
          >
            <FileCode className="w-4 h-4 text-emerald-400" />
            HTML Document
          </button>
          <button
            onClick={() => {
              onPrint();
              setOpen(false);
            }}
            className="w-full text-left px-3 py-2 rounded-lg hover:bg-slate-800 text-slate-200 transition flex items-center gap-2"
          >
            <Printer className="w-4 h-4 text-purple-400" />
            Print / Save PDF
          </button>
          <button
            onClick={() => handleDownload('json')}
            className="w-full text-left px-3 py-2 rounded-lg hover:bg-slate-800 text-slate-200 transition flex items-center gap-2 border-t border-slate-800 pt-2"
          >
            <Code className="w-4 h-4 text-amber-400" />
            Structured JSON
          </button>
        </div>
      )}
    </div>
  );
};
