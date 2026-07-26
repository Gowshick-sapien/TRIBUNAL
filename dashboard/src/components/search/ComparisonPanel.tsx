import React from 'react';
import { Columns, ArrowLeftRight } from 'lucide-react';
import type { SearchResultItem } from '../../types/search';
import { RiskChip } from '../common/RiskChip';
import { ConfidenceMeter } from '../common/ConfidenceMeter';

interface ComparisonPanelProps {
  itemA: SearchResultItem | null;
  itemB: SearchResultItem | null;
  onNavigateViewer: (id: string) => void;
  onNavigateGraph: (id: string) => void;
}

export const ComparisonPanel: React.FC<ComparisonPanelProps> = ({
  itemA,
  itemB,
  onNavigateViewer,
  onNavigateGraph,
}) => {
  if (!itemA || !itemB) {
    return (
      <div className="surface-card p-12 rounded-lg border border-slate-200 text-center font-sans text-xs text-slate-500 space-y-2">
        <Columns className="w-8 h-8 text-blue-600 mx-auto" />
        <p className="font-semibold text-slate-900 text-sm">Side-by-Side Comparison Workspace</p>
        <p>Please select exactly two investigations from the Repository Explorer table using the compare checkboxes.</p>
      </div>
    );
  }

  return (
    <div className="space-y-6 font-sans">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-200 pb-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <ArrowLeftRight className="w-5 h-5 text-blue-600" />
            Compare <span className="font-mono text-blue-600">{itemA.id}</span> <span className="text-slate-400 font-sans text-sm font-normal">vs</span> <span className="font-mono text-slate-700">{itemB.id}</span>
          </h2>
          <p className="text-xs text-slate-500 mt-1">
            Side-by-side analysis across risk, confidence, recommendations, and graph topology.
          </p>
        </div>
      </div>

      {/* Comparison Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Investigation A Card */}
        <div className="surface-card p-6 rounded-lg border border-slate-200 space-y-5 shadow-xs">
          <div className="flex items-center justify-between border-b border-slate-200 pb-3">
            <div>
              <span className="text-[10px] font-sans font-semibold text-blue-600 uppercase tracking-wider">Investigation A</span>
              <h3 className="text-base font-semibold text-slate-900 font-mono">{itemA.id}</h3>
            </div>
            <RiskChip risk={itemA.risk_level} />
          </div>

          <div className="space-y-1.5">
            <span className="text-[10px] font-sans font-semibold text-slate-500 uppercase tracking-wider">Target Query</span>
            <p className="text-xs font-sans text-slate-800 bg-slate-50 p-3 rounded-md border border-slate-200">
              {itemA.query}
            </p>
          </div>

          <div className="space-y-1.5">
            <span className="text-[10px] font-sans font-semibold text-slate-500 uppercase tracking-wider">Winning Hypothesis</span>
            <p className="text-xs font-sans font-semibold text-slate-900 bg-slate-50 p-3 rounded-md border border-slate-200">
              {itemA.winning_hypothesis || 'Structuring Activity'}
            </p>
          </div>

          <div className="space-y-1.5">
            <span className="text-[10px] font-sans font-semibold text-slate-500 uppercase tracking-wider">Calibrated Confidence</span>
            <ConfidenceMeter confidence={itemA.confidence} />
          </div>

          <div className="space-y-1.5">
            <span className="text-[10px] font-sans font-semibold text-slate-500 uppercase tracking-wider">Recommendation</span>
            <p className="text-xs font-sans text-slate-700 bg-slate-50 p-3 rounded-md border border-slate-200 leading-relaxed">
              {itemA.recommendation}
            </p>
          </div>

          <div className="grid grid-cols-2 gap-2 text-xs font-sans pt-2 border-t border-slate-200">
            <div>
              <span className="text-slate-500 text-[10px] block font-medium">Dataset</span>
              <span className="text-slate-900 font-semibold font-mono">{itemA.dataset}</span>
            </div>
            <div>
              <span className="text-slate-500 text-[10px] block font-medium">Topology</span>
              <span className="text-slate-900 font-semibold font-mono">{itemA.node_count} Nodes / {itemA.edge_count} Edges</span>
            </div>
          </div>

          <div className="flex gap-2 pt-2">
            <button
              onClick={() => onNavigateViewer(itemA.id)}
              className="flex-1 py-2 rounded-md bg-blue-600 hover:bg-blue-700 text-white font-medium text-xs transition-colors shadow-xs"
            >
              View Investigation A
            </button>
            <button
              onClick={() => onNavigateGraph(itemA.id)}
              className="flex-1 py-2 rounded-md bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 font-medium text-xs transition-colors shadow-xs"
            >
              View Graph A
            </button>
          </div>
        </div>

        {/* Investigation B Card */}
        <div className="surface-card p-6 rounded-lg border border-slate-200 space-y-5 shadow-xs">
          <div className="flex items-center justify-between border-b border-slate-200 pb-3">
            <div>
              <span className="text-[10px] font-sans font-semibold text-slate-600 uppercase tracking-wider">Investigation B</span>
              <h3 className="text-base font-semibold text-slate-900 font-mono">{itemB.id}</h3>
            </div>
            <RiskChip risk={itemB.risk_level} />
          </div>

          <div className="space-y-1.5">
            <span className="text-[10px] font-sans font-semibold text-slate-500 uppercase tracking-wider">Target Query</span>
            <p className="text-xs font-sans text-slate-800 bg-slate-50 p-3 rounded-md border border-slate-200">
              {itemB.query}
            </p>
          </div>

          <div className="space-y-1.5">
            <span className="text-[10px] font-sans font-semibold text-slate-500 uppercase tracking-wider">Winning Hypothesis</span>
            <p className="text-xs font-sans font-semibold text-slate-900 bg-slate-50 p-3 rounded-md border border-slate-200">
              {itemB.winning_hypothesis || 'High Velocity Anomaly'}
            </p>
          </div>

          <div className="space-y-1.5">
            <span className="text-[10px] font-sans font-semibold text-slate-500 uppercase tracking-wider">Calibrated Confidence</span>
            <ConfidenceMeter confidence={itemB.confidence} />
          </div>

          <div className="space-y-1.5">
            <span className="text-[10px] font-sans font-semibold text-slate-500 uppercase tracking-wider">Recommendation</span>
            <p className="text-xs font-sans text-slate-700 bg-slate-50 p-3 rounded-md border border-slate-200 leading-relaxed">
              {itemB.recommendation}
            </p>
          </div>

          <div className="grid grid-cols-2 gap-2 text-xs font-sans pt-2 border-t border-slate-200">
            <div>
              <span className="text-slate-500 text-[10px] block font-medium">Dataset</span>
              <span className="text-slate-900 font-semibold font-mono">{itemB.dataset}</span>
            </div>
            <div>
              <span className="text-slate-500 text-[10px] block font-medium">Topology</span>
              <span className="text-slate-900 font-semibold font-mono">{itemB.node_count} Nodes / {itemB.edge_count} Edges</span>
            </div>
          </div>

          <div className="flex gap-2 pt-2">
            <button
              onClick={() => onNavigateViewer(itemB.id)}
              className="flex-1 py-2 rounded-md bg-blue-600 hover:bg-blue-700 text-white font-medium text-xs transition-colors shadow-xs"
            >
              View Investigation B
            </button>
            <button
              onClick={() => onNavigateGraph(itemB.id)}
              className="flex-1 py-2 rounded-md bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 font-medium text-xs transition-colors shadow-xs"
            >
              View Graph B
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

