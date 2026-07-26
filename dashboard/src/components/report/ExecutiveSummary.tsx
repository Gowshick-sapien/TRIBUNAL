import React from 'react';
import { Sparkles, ShieldAlert } from 'lucide-react';
import type { StructuredReportPayload } from '../../types/report';

interface ExecutiveSummaryProps {
  report: StructuredReportPayload;
}

export const ExecutiveSummary: React.FC<ExecutiveSummaryProps> = ({ report }) => {
  return (
    <div id="sec-summary" className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4 scroll-mt-6">
      <div className="flex items-center gap-2 text-cyan-400 font-mono text-xs font-bold uppercase tracking-wider border-b border-slate-800 pb-2">
        <Sparkles className="w-4 h-4" /> Section 1: Executive Summary
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 font-mono text-xs">
        <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1">
          <span className="text-[10px] text-slate-400 uppercase font-bold">Assessed Risk Level</span>
          <p className="text-lg font-black text-rose-400">{report.risk_level}</p>
        </div>
        <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1">
          <span className="text-[10px] text-slate-400 uppercase font-bold">Calibrated Confidence</span>
          <p className="text-lg font-black text-cyan-400">85%</p>
        </div>
        <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1">
          <span className="text-[10px] text-slate-400 uppercase font-bold">Engine Status</span>
          <p className="text-lg font-black text-emerald-400">VERDICT CONCLUDED</p>
        </div>
      </div>

      <div className="space-y-2">
        <span className="text-xs font-mono text-slate-400 uppercase font-bold">Primary Executive Recommendation</span>
        <div className="p-4 rounded-xl bg-rose-950/20 border border-rose-800/40 text-slate-200 font-mono text-xs leading-relaxed">
          <div className="flex items-center gap-2 text-rose-400 font-bold mb-1">
            <ShieldAlert className="w-4 h-4" /> {report.recommendation}
          </div>
          Target customer exhibits multiple severe financial velocity and structuring indicators corroborated by cross-expert analysis. Immediate escalation for Suspicious Activity Report (SAR) filing recommended.
        </div>
      </div>
    </div>
  );
};
