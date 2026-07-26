import React from 'react';
import { Layers, ArrowLeftRight } from 'lucide-react';
import { RiskChip } from '../common/RiskChip';
import { ConfidenceMeter } from '../common/ConfidenceMeter';
import { ExportMenu } from './ExportMenu';

interface ReportHeaderProps {
  id: string;
  generatedAt: string;
  riskLevel: string;
  confidence: number;
  recommendation: string;
  dataset: string;
  onNavigateGraph: () => void;
  onNavigateCompare: () => void;
  onPrint: () => void;
}

export const ReportHeader: React.FC<ReportHeaderProps> = ({
  id,
  generatedAt,
  riskLevel,
  confidence,
  recommendation,
  dataset,
  onNavigateGraph,
  onNavigateCompare,
  onPrint,
}) => {
  return (
    <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <div className="flex items-center gap-3">
            <span className="text-xs font-mono text-cyan-400 font-bold bg-cyan-950/60 px-2.5 py-1 rounded border border-cyan-800">
              CASE: {id}
            </span>
            <RiskChip risk={riskLevel} />
          </div>
          <h1 className="text-xl font-black text-slate-100 font-sans tracking-tight mt-2">
            Interactive Investigation & Compliance Report
          </h1>
          <p className="text-xs font-mono text-slate-400 mt-1">
            Generated on {new Date(generatedAt).toLocaleString()} • Dataset: <span className="text-slate-200 font-bold">{dataset}</span>
          </p>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-wrap items-center gap-2 font-mono text-xs">
          <ExportMenu reportId={id} onPrint={onPrint} />

          <button
            onClick={onNavigateGraph}
            className="px-3.5 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-200 font-bold transition flex items-center gap-1.5"
          >
            <Layers className="w-4 h-4 text-cyan-400" />
            Open Graph (D.4)
          </button>

          <button
            onClick={onNavigateCompare}
            className="px-3.5 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-200 font-bold transition flex items-center gap-1.5"
          >
            <ArrowLeftRight className="w-4 h-4 text-purple-400" />
            Compare
          </button>
        </div>
      </div>

      {/* Confidence & Recommendation Meter */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 items-center">
        <div className="space-y-1">
          <span className="text-[10px] font-mono text-slate-400 uppercase font-bold">Calibrated Confidence Score</span>
          <ConfidenceMeter confidence={confidence} />
        </div>
        <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800 font-mono text-xs">
          <span className="text-[10px] text-slate-400 uppercase font-bold block mb-1">Recommendation</span>
          <span className="text-cyan-300 font-bold">{recommendation}</span>
        </div>
      </div>
    </div>
  );
};
