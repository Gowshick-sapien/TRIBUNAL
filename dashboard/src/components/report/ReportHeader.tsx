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
    <div className="surface-card p-6 rounded-lg border border-slate-200 space-y-4 shadow-xs font-sans">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 pb-4">
        <div>
          <div className="flex items-center gap-3">
            <span className="text-xs font-mono text-slate-700 font-semibold bg-slate-100 px-2.5 py-0.5 rounded border border-slate-200">
              CASE: {id}
            </span>
            <RiskChip risk={riskLevel} />
          </div>
          <h1 className="text-xl font-bold text-slate-900 tracking-tight mt-2">
            Interactive Investigation & Compliance Report
          </h1>
          <p className="text-xs text-slate-500 font-sans mt-1">
            Generated on {new Date(generatedAt).toLocaleString()} • Dataset: <span className="text-slate-900 font-semibold font-mono">{dataset}</span>
          </p>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-wrap items-center gap-2 font-sans text-xs">
          <ExportMenu reportId={id} onPrint={onPrint} />

          <button
            onClick={onNavigateGraph}
            className="px-3 py-1.5 rounded-md bg-white hover:bg-slate-50 border border-slate-200 text-slate-700 font-medium transition-colors flex items-center gap-1.5 shadow-xs"
          >
            <Layers className="w-3.5 h-3.5 text-blue-600" />
            Open Graph
          </button>

          <button
            onClick={onNavigateCompare}
            className="px-3 py-1.5 rounded-md bg-white hover:bg-slate-50 border border-slate-200 text-slate-700 font-medium transition-colors flex items-center gap-1.5 shadow-xs"
          >
            <ArrowLeftRight className="w-3.5 h-3.5 text-slate-600" />
            Compare
          </button>
        </div>
      </div>

      {/* Confidence & Recommendation Meter */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 items-center">
        <div className="space-y-1">
          <span className="text-[10px] font-sans font-semibold text-slate-500 uppercase tracking-wider">Calibrated Confidence Score</span>
          <ConfidenceMeter confidence={confidence} />
        </div>
        <div className="p-3 rounded-md bg-slate-50 border border-slate-200 font-sans text-xs">
          <span className="text-[10px] text-slate-500 uppercase font-semibold block mb-1">Recommendation</span>
          <span className="text-slate-900 font-semibold">{recommendation}</span>
        </div>
      </div>
    </div>
  );
};
