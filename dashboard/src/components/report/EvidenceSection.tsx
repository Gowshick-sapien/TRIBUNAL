import React from 'react';
import { Layers, ArrowRight } from 'lucide-react';
import type { EvidenceCardItem } from '../../types/report';

interface EvidenceSectionProps {
  evidenceCards?: EvidenceCardItem[];
  onNavigateGraph: (cardId?: string) => void;
}

export const EvidenceSection: React.FC<EvidenceSectionProps> = ({
  evidenceCards = [
    {
      id: 'c_fin_structuring_01',
      expert: 'Financial Expert',
      hypothesis: 'Account engaged in structured cash deposits below $10,000 threshold',
      confidence: 0.88,
      severity: 'CRITICAL',
      supporting_transactions: ['TX_80001', 'TX_80002', 'TX_80003'],
    },
    {
      id: 'c_beh_velocity_02',
      expert: 'Behaviour Expert',
      hypothesis: 'Sudden 400% surge in transaction frequency after 90 days of dormancy',
      confidence: 0.82,
      severity: 'HIGH',
      supporting_transactions: ['TX_80045', 'TX_80046'],
    },
  ],
  onNavigateGraph,
}) => {
  return (
    <div id="sec-evidence" className="surface-card p-6 rounded-lg border border-slate-200 space-y-4 scroll-mt-6 shadow-xs font-sans">
      <div className="flex items-center justify-between border-b border-slate-200 pb-2.5 font-sans text-xs">
        <span className="text-blue-600 font-semibold uppercase tracking-wider flex items-center gap-2">
          <Layers className="w-4 h-4 text-blue-600" /> Section 5: Evidence Cards & Topology
        </span>
        <button
          onClick={() => onNavigateGraph()}
          className="text-blue-600 hover:text-blue-700 font-medium flex items-center gap-1 transition-colors"
        >
          Open Graph Studio <ArrowRight className="w-3.5 h-3.5" />
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {evidenceCards.map((card) => (
          <div key={card.id} className="surface-card p-4 rounded-lg border border-slate-200 space-y-3 font-sans text-xs shadow-xs">
            <div className="flex items-center justify-between">
              <span className="font-mono font-semibold text-blue-600">{card.id}</span>
              <span className="px-2 py-0.5 rounded bg-rose-50 text-rose-700 border border-rose-200 font-mono font-medium text-[10px]">
                {card.severity}
              </span>
            </div>

            <div className="text-slate-800 font-sans text-xs leading-relaxed">{card.hypothesis}</div>

            <div className="flex items-center justify-between pt-2.5 border-t border-slate-200 text-[11px]">
              <span className="text-slate-500">Source: <strong className="text-slate-700 font-medium">{card.expert}</strong></span>
              <button
                onClick={() => onNavigateGraph(card.id)}
                className="text-blue-600 hover:text-blue-700 font-medium flex items-center gap-1 text-[11px] transition-colors"
              >
                Highlight Node in Graph &rarr;
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
