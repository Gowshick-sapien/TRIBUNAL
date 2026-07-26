import React from 'react';
import { Gavel, CheckCircle2 } from 'lucide-react';

interface TribunalSectionProps {
  winningHypothesis?: string;
  runnerUp?: string;
  confidenceGap?: number;
  supportMargin?: number;
}

export const TribunalSection: React.FC<TribunalSectionProps> = ({
  winningHypothesis = 'Financial Structuring & Velocity Anomaly',
  runnerUp = 'Unusual High Volume Transfer',
  confidenceGap = 0.42,
  supportMargin = 0.65,
}) => {
  return (
    <div id="sec-tribunal" className="surface-card p-6 rounded-lg border border-slate-200 space-y-4 scroll-mt-6 shadow-xs font-sans">
      <div className="text-blue-600 font-sans text-xs font-semibold uppercase tracking-wider border-b border-slate-200 pb-2.5 flex items-center gap-2">
        <Gavel className="w-4 h-4 text-blue-600" /> Section 7: Tribunal Deliberation & Verdict Consensus
      </div>

      <div className="p-4 rounded-lg bg-blue-50/60 border border-blue-200 space-y-3 font-sans text-xs">
        <div className="flex items-center gap-2 text-slate-900 font-semibold text-sm">
          <CheckCircle2 className="w-5 h-5 text-blue-600" />
          Winning Consensus Hypothesis: <span className="text-blue-700">{winningHypothesis}</span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-2.5 border-t border-blue-200/80">
          <div>
            <span className="text-[10px] text-slate-500 block uppercase font-medium">Runner-Up Hypothesis</span>
            <span className="text-slate-900 font-semibold">{runnerUp}</span>
          </div>
          <div>
            <span className="text-[10px] text-slate-500 block uppercase font-medium">Confidence Gap Margin</span>
            <span className="text-blue-600 font-mono font-semibold">{(confidenceGap * 100).toFixed(0)}%</span>
          </div>
          <div>
            <span className="text-[10px] text-slate-500 block uppercase font-medium">Support Score</span>
            <span className="text-emerald-700 font-mono font-semibold">{(supportMargin * 100).toFixed(0)}%</span>
          </div>
        </div>
      </div>
    </div>
  );
};
