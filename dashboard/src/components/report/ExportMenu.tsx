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
        className="px-3.5 py-1.5 rounded-md bg-blue-600 hover:bg-blue-700 text-white font-medium font-sans text-xs transition-colors flex items-center gap-1.5 shadow-xs"
      >
        <Download className="w-3.5 h-3.5" />
        Export Report
      </button>

      {open && (
        <div className="absolute right-0 mt-2 w-48 bg-white border border-slate-200 rounded-lg p-1 shadow-lg z-50 font-sans text-xs space-y-0.5">
          <button
            onClick={() => handleDownload('markdown')}
            className="w-full text-left px-3 py-2 rounded-md hover:bg-slate-50 text-slate-700 transition-colors flex items-center gap-2 font-medium"
          >
            <FileText className="w-3.5 h-3.5 text-blue-600" />
            Markdown (.md)
          </button>
          <button
            onClick={() => handleDownload('html')}
            className="w-full text-left px-3 py-2 rounded-md hover:bg-slate-50 text-slate-700 transition-colors flex items-center gap-2 font-medium"
          >
            <FileCode className="w-3.5 h-3.5 text-emerald-600" />
            HTML Document
          </button>
          <button
            onClick={() => {
              onPrint();
              setOpen(false);
            }}
            className="w-full text-left px-3 py-2 rounded-md hover:bg-slate-50 text-slate-700 transition-colors flex items-center gap-2 font-medium"
          >
            <Printer className="w-3.5 h-3.5 text-slate-600" />
            Print / Save PDF
          </button>
          <button
            onClick={() => handleDownload('json')}
            className="w-full text-left px-3 py-2 rounded-md hover:bg-slate-50 text-slate-700 transition-colors flex items-center gap-2 font-medium border-t border-slate-100 pt-2"
          >
            <Code className="w-3.5 h-3.5 text-amber-600" />
            Structured JSON
          </button>
        </div>
      )}
    </div>
  );
};
