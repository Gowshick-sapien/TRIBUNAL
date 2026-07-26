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
    <div id="sec-evidence" className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4 scroll-mt-6">
      <div className="flex items-center justify-between border-b border-slate-800 pb-2 font-mono text-xs">
        <span className="text-cyan-400 font-bold uppercase tracking-wider flex items-center gap-2">
          <Layers className="w-4 h-4" /> Section 5: Evidence Cards & Topology
        </span>
        <button
          onClick={() => onNavigateGraph()}
          className="text-cyan-400 hover:underline font-bold flex items-center gap-1"
        >
          Open Graph Studio (D.4) <ArrowRight className="w-3 h-3" />
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {evidenceCards.map((card) => (
          <div key={card.id} className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 space-y-3 font-mono text-xs">
            <div className="flex items-center justify-between">
              <span className="font-bold text-cyan-400">{card.id}</span>
              <span className="px-2 py-0.5 rounded bg-rose-950 text-rose-300 border border-rose-800 font-bold text-[10px]">
                {card.severity}
              </span>
            </div>

            <div className="text-slate-300 font-sans text-xs">{card.hypothesis}</div>

            <div className="flex items-center justify-between pt-2 border-t border-slate-800/80 text-[11px]">
              <span className="text-slate-400">Source: <strong className="text-slate-200">{card.expert}</strong></span>
              <button
                onClick={() => onNavigateGraph(card.id)}
                className="text-cyan-400 hover:text-cyan-300 font-bold flex items-center gap-1 text-[11px]"
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
