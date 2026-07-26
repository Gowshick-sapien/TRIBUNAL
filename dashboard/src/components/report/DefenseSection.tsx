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
    <div id="sec-defense" className="surface-card p-6 rounded-lg border border-slate-200 space-y-4 scroll-mt-6 shadow-xs font-sans">
      <div className="text-blue-600 font-sans text-xs font-semibold uppercase tracking-wider border-b border-slate-200 pb-2.5 flex items-center gap-2">
        <ShieldCheck className="w-4 h-4 text-blue-600" /> Section 6: Adversarial Defense & Counter-Hypothesis Evaluation
      </div>

      <div className="space-y-3 font-sans text-xs">
        {defenseItems.map((item, idx) => (
          <div key={idx} className="p-4 rounded-lg bg-slate-50 border border-slate-200 space-y-2">
            <div className="flex items-center justify-between">
              <span className="font-semibold text-slate-900">{item.counter_hypothesis}</span>
              <span className="px-2 py-0.5 rounded bg-rose-50 text-rose-700 border border-rose-200 font-mono font-medium text-[10px] flex items-center gap-1">
                <ShieldAlert className="w-3 h-3" /> {item.status}
              </span>
            </div>
            <p className="text-slate-600 font-sans text-xs leading-relaxed">{item.reasoning}</p>
          </div>
        ))}
      </div>
    </div>
  );
};
