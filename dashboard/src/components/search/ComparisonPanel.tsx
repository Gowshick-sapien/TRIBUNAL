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
      <div className="glass-panel p-12 rounded-2xl border border-slate-800 text-center font-mono text-xs text-slate-500 space-y-2">
        <Columns className="w-8 h-8 text-cyan-400 mx-auto" />
        <p className="font-bold text-slate-300">Side-by-Side Comparison Workspace</p>
        <p>Please select exactly two investigations from the Repository Explorer table using the compare checkboxes.</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h2 className="text-xl font-black text-slate-100 font-sans tracking-tight flex items-center gap-2">
            <ArrowLeftRight className="w-5 h-5 text-cyan-400" />
            Compare <span className="text-cyan-400 font-mono">{itemA.id}</span> <span className="text-slate-500 font-mono text-sm font-normal">vs</span> <span className="text-purple-400 font-mono">{itemB.id}</span>
          </h2>
          <p className="text-xs font-mono text-slate-400 mt-1">
            Side-by-side analysis across risk, confidence, recommendations, and graph topology.
          </p>
        </div>
      </div>

      {/* Comparison Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Investigation A Card */}
        <div className="glass-panel p-6 rounded-2xl border border-cyan-500/40 space-y-5">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <div>
              <span className="text-[10px] font-mono font-bold text-cyan-400 uppercase">Investigation A</span>
              <h3 className="text-base font-bold text-slate-100 font-mono">{itemA.id}</h3>
            </div>
            <RiskChip risk={itemA.risk_level} />
          </div>

          <div className="space-y-2">
            <span className="text-xs font-mono text-slate-400 uppercase">Target Query</span>
            <p className="text-xs font-sans text-slate-200 bg-slate-900/60 p-3 rounded-lg border border-slate-800">
              {itemA.query}
            </p>
          </div>

          <div className="space-y-2">
            <span className="text-xs font-mono text-slate-400 uppercase">Winning Hypothesis</span>
            <p className="text-xs font-sans font-bold text-cyan-300 bg-slate-900/60 p-3 rounded-lg border border-slate-800">
              {itemA.winning_hypothesis || 'Structuring Activity'}
            </p>
          </div>

          <div className="space-y-2">
            <span className="text-xs font-mono text-slate-400 uppercase">Calibrated Confidence</span>
            <ConfidenceMeter confidence={itemA.confidence} />
          </div>

          <div className="space-y-2">
            <span className="text-xs font-mono text-slate-400 uppercase">Recommendation</span>
            <p className="text-xs font-mono text-slate-300 bg-slate-900/60 p-3 rounded-lg border border-slate-800">
              {itemA.recommendation}
            </p>
          </div>

          <div className="grid grid-cols-2 gap-2 text-xs font-mono pt-2 border-t border-slate-800">
            <div>
              <span className="text-slate-500 text-[10px] block">Dataset</span>
              <span className="text-slate-200 font-bold">{itemA.dataset}</span>
            </div>
            <div>
              <span className="text-slate-500 text-[10px] block">Topology</span>
              <span className="text-cyan-400 font-bold">{itemA.node_count} Nodes / {itemA.edge_count} Edges</span>
            </div>
          </div>

          <div className="flex gap-2 pt-2">
            <button
              onClick={() => onNavigateViewer(itemA.id)}
              className="flex-1 py-2 rounded-lg bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-mono font-bold text-xs transition"
            >
              View Investigation A
            </button>
            <button
              onClick={() => onNavigateGraph(itemA.id)}
              className="flex-1 py-2 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-700 font-mono text-xs transition"
            >
              View Graph A
            </button>
          </div>
        </div>

        {/* Investigation B Card */}
        <div className="glass-panel p-6 rounded-2xl border border-purple-500/40 space-y-5">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <div>
              <span className="text-[10px] font-mono font-bold text-purple-400 uppercase">Investigation B</span>
              <h3 className="text-base font-bold text-slate-100 font-mono">{itemB.id}</h3>
            </div>
            <RiskChip risk={itemB.risk_level} />
          </div>

          <div className="space-y-2">
            <span className="text-xs font-mono text-slate-400 uppercase">Target Query</span>
            <p className="text-xs font-sans text-slate-200 bg-slate-900/60 p-3 rounded-lg border border-slate-800">
              {itemB.query}
            </p>
          </div>

          <div className="space-y-2">
            <span className="text-xs font-mono text-slate-400 uppercase">Winning Hypothesis</span>
            <p className="text-xs font-sans font-bold text-purple-300 bg-slate-900/60 p-3 rounded-lg border border-slate-800">
              {itemB.winning_hypothesis || 'High Velocity Anomaly'}
            </p>
          </div>

          <div className="space-y-2">
            <span className="text-xs font-mono text-slate-400 uppercase">Calibrated Confidence</span>
            <ConfidenceMeter confidence={itemB.confidence} />
          </div>

          <div className="space-y-2">
            <span className="text-xs font-mono text-slate-400 uppercase">Recommendation</span>
            <p className="text-xs font-mono text-slate-300 bg-slate-900/60 p-3 rounded-lg border border-slate-800">
              {itemB.recommendation}
            </p>
          </div>

          <div className="grid grid-cols-2 gap-2 text-xs font-mono pt-2 border-t border-slate-800">
            <div>
              <span className="text-slate-500 text-[10px] block">Dataset</span>
              <span className="text-slate-200 font-bold">{itemB.dataset}</span>
            </div>
            <div>
              <span className="text-slate-500 text-[10px] block">Topology</span>
              <span className="text-purple-400 font-bold">{itemB.node_count} Nodes / {itemB.edge_count} Edges</span>
            </div>
          </div>

          <div className="flex gap-2 pt-2">
            <button
              onClick={() => onNavigateViewer(itemB.id)}
              className="flex-1 py-2 rounded-lg bg-purple-500 hover:bg-purple-400 text-slate-950 font-mono font-bold text-xs transition"
            >
              View Investigation B
            </button>
            <button
              onClick={() => onNavigateGraph(itemB.id)}
              className="flex-1 py-2 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-700 font-mono text-xs transition"
            >
              View Graph B
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
