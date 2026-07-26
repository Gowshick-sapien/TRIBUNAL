import React from 'react';
import { Sparkles, ShieldAlert } from 'lucide-react';
import type { StructuredReportPayload } from '../../types/report';

interface ExecutiveSummaryProps {
  report: StructuredReportPayload;
}

export const ExecutiveSummary: React.FC<ExecutiveSummaryProps> = ({ report }) => {
  return (
    <div id="sec-summary" className="surface-card p-6 rounded-lg border border-slate-200 space-y-4 scroll-mt-6 shadow-xs font-sans">
      <div className="flex items-center gap-2 text-blue-600 font-sans text-xs font-semibold uppercase tracking-wider border-b border-slate-200 pb-2.5">
        <Sparkles className="w-4 h-4 text-blue-600" /> Section 1: Executive Summary
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 font-sans text-xs">
        <div className="p-4 rounded-md bg-slate-50 border border-slate-200 space-y-1">
          <span className="text-[10px] text-slate-500 uppercase font-semibold">Assessed Risk Level</span>
          <p className="text-lg font-bold text-rose-700 font-mono">{report.risk_level}</p>
        </div>
        <div className="p-4 rounded-md bg-slate-50 border border-slate-200 space-y-1">
          <span className="text-[10px] text-slate-500 uppercase font-semibold">Calibrated Confidence</span>
          <p className="text-lg font-bold text-blue-600 font-mono">85%</p>
        </div>
        <div className="p-4 rounded-md bg-slate-50 border border-slate-200 space-y-1">
          <span className="text-[10px] text-slate-500 uppercase font-semibold">Engine Status</span>
          <p className="text-lg font-bold text-emerald-700 font-mono">VERDICT CONCLUDED</p>
        </div>
      </div>

      <div className="space-y-2">
        <span className="text-xs font-sans text-slate-500 uppercase font-semibold">Primary Executive Recommendation</span>
        <div className="p-4 rounded-md bg-rose-50 border border-rose-200 text-slate-800 font-sans text-xs leading-relaxed space-y-1">
          <div className="flex items-center gap-2 text-rose-700 font-semibold">
            <ShieldAlert className="w-4 h-4" /> {report.recommendation}
          </div>
          <p className="text-slate-700">
            Target customer exhibits multiple severe financial velocity and structuring indicators corroborated by cross-expert analysis. Immediate escalation for Suspicious Activity Report (SAR) filing recommended.
          </p>
        </div>
      </div>
    </div>
  );
};
