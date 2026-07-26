import React from 'react';
import { Activity } from 'lucide-react';
import type { EvidenceGraphPayload } from '../../types/graph';

interface GraphMetricsProps {
  statistics: EvidenceGraphPayload['statistics'];
}

export const GraphMetrics: React.FC<GraphMetricsProps> = ({ statistics }) => {
  return (
    <div className="glass-panel p-4 rounded-xl border border-slate-800 space-y-3 font-mono text-xs shadow-lg max-w-sm">
      <div className="flex items-center justify-between border-b border-slate-800 pb-2">
        <h4 className="font-bold text-slate-300 uppercase tracking-wider flex items-center gap-1.5 text-[11px]">
          <Activity className="w-3.5 h-3.5 text-cyan-400" />
          Evidence Topology Metrics
        </h4>
        <span className="text-[10px] px-2 py-0.5 rounded bg-cyan-950 text-cyan-300 border border-cyan-800">
          Phase C Graph
        </span>
      </div>

      <div className="grid grid-cols-2 gap-3">
        <div className="p-2.5 rounded bg-slate-900/80 border border-slate-800">
          <span className="text-[10px] text-slate-400 block">Total Nodes</span>
          <span className="text-base font-bold text-cyan-400">{statistics.node_count}</span>
        </div>
        <div className="p-2.5 rounded bg-slate-900/80 border border-slate-800">
          <span className="text-[10px] text-slate-400 block">Total Edges</span>
          <span className="text-base font-bold text-cyan-400">{statistics.edge_count}</span>
        </div>
        <div className="p-2.5 rounded bg-slate-900/80 border border-slate-800">
          <span className="text-[10px] text-slate-400 block">Density</span>
          <span className="text-base font-bold text-emerald-400">
            {statistics.density.toFixed(3)}
          </span>
        </div>
        <div className="p-2.5 rounded bg-slate-900/80 border border-slate-800">
          <span className="text-[10px] text-slate-400 block">Avg Degree</span>
          <span className="text-base font-bold text-cyan-400">
            {statistics.average_degree ? statistics.average_degree.toFixed(2) : '1.5'}
          </span>
        </div>
      </div>
    </div>
  );
};
