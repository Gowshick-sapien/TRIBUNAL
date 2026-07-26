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
    <div id="sec-tribunal" className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4 scroll-mt-6">
      <div className="text-cyan-400 font-mono text-xs font-bold uppercase tracking-wider border-b border-slate-800 pb-2 flex items-center gap-2">
        <Gavel className="w-4 h-4" /> Section 7: Tribunal Deliberation & Verdict Consensus
      </div>

      <div className="p-4 rounded-xl bg-cyan-950/20 border border-cyan-800/40 space-y-3 font-mono text-xs">
        <div className="flex items-center gap-2 text-cyan-400 font-bold text-sm">
          <CheckCircle2 className="w-5 h-5 text-cyan-400" />
          Winning Consensus Hypothesis: {winningHypothesis}
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-2 border-t border-slate-800">
          <div>
            <span className="text-[10px] text-slate-500 block">Runner-Up Hypothesis</span>
            <span className="text-slate-300 font-bold">{runnerUp}</span>
          </div>
          <div>
            <span className="text-[10px] text-slate-500 block">Confidence Gap Margin</span>
            <span className="text-cyan-400 font-bold">{(confidenceGap * 100).toFixed(0)}%</span>
          </div>
          <div>
            <span className="text-[10px] text-slate-500 block">Support Score</span>
            <span className="text-emerald-400 font-bold">{(supportMargin * 100).toFixed(0)}%</span>
          </div>
        </div>
      </div>
    </div>
  );
};
