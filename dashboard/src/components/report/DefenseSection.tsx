import React from 'react';
import { ShieldCheck, ShieldAlert } from 'lucide-react';
import type { DefenseItem } from '../../types/report';

interface DefenseSectionProps {
  defenseItems?: DefenseItem[];
}

export const DefenseSection: React.FC<DefenseSectionProps> = ({
  defenseItems = [
    {
      counter_hypothesis: 'Legitimate Payroll Disbursement Activity',
      status: 'REJECTED',
      reasoning: 'Transactions occur in round amounts ($9,990) to unverified personal accounts rather than corporate payroll batches.',
      confidence: 0.15,
    },
    {
      counter_hypothesis: 'Standard Seasonal Liquidity Movement',
      status: 'REJECTED',
      reasoning: 'Historical 12-month baseline reveals no prior seasonal surge during this calendar period.',
      confidence: 0.20,
    },
  ],
}) => {
  return (
    <div id="sec-defense" className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4 scroll-mt-6">
      <div className="text-cyan-400 font-mono text-xs font-bold uppercase tracking-wider border-b border-slate-800 pb-2 flex items-center gap-2">
        <ShieldCheck className="w-4 h-4" /> Section 6: Adversarial Defense & Counter-Hypothesis Evaluation
      </div>

      <div className="space-y-3 font-mono text-xs">
        {defenseItems.map((item, idx) => (
          <div key={idx} className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 space-y-2">
            <div className="flex items-center justify-between">
              <span className="font-bold text-slate-200">{item.counter_hypothesis}</span>
              <span className="px-2 py-0.5 rounded bg-rose-950 text-rose-300 border border-rose-800 font-bold text-[10px] flex items-center gap-1">
                <ShieldAlert className="w-3 h-3" /> {item.status}
              </span>
            </div>
            <p className="text-slate-400 font-sans text-xs leading-relaxed">{item.reasoning}</p>
          </div>
        ))}
      </div>
    </div>
  );
};
