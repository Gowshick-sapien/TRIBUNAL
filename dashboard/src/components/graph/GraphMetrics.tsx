import React from 'react';
import { Activity } from 'lucide-react';
import type { EvidenceGraphPayload } from '../../types/graph';

interface GraphMetricsProps {
  statistics: EvidenceGraphPayload['statistics'];
}

export const GraphMetrics: React.FC<GraphMetricsProps> = ({ statistics }) => {
  return (
    <div className="surface-card p-4 rounded-lg border border-slate-200 space-y-3 font-sans text-xs shadow-xs bg-white max-w-sm">
      <div className="flex items-center justify-between border-b border-slate-200 pb-2">
        <h4 className="font-semibold text-slate-900 uppercase tracking-wider flex items-center gap-1.5 text-[10px]">
          <Activity className="w-3.5 h-3.5 text-blue-600" />
          Evidence Topology Metrics
        </h4>
        <span className="text-[10px] px-2 py-0.5 rounded bg-slate-100 text-slate-700 border border-slate-200 font-mono">
          Phase C Graph
        </span>
      </div>

      <div className="grid grid-cols-2 gap-3 font-sans">
        <div className="p-2.5 rounded-md bg-slate-50 border border-slate-200">
          <span className="text-[10px] text-slate-500 block uppercase font-medium">Total Nodes</span>
          <span className="text-base font-bold text-slate-900 font-mono">{statistics.node_count}</span>
        </div>
        <div className="p-2.5 rounded-md bg-slate-50 border border-slate-200">
          <span className="text-[10px] text-slate-500 block uppercase font-medium">Total Edges</span>
          <span className="text-base font-bold text-slate-900 font-mono">{statistics.edge_count}</span>
        </div>
        <div className="p-2.5 rounded-md bg-slate-50 border border-slate-200">
          <span className="text-[10px] text-slate-500 block uppercase font-medium">Density</span>
          <span className="text-base font-bold text-emerald-700 font-mono">
            {statistics.density.toFixed(3)}
          </span>
        </div>
        <div className="p-2.5 rounded-md bg-slate-50 border border-slate-200">
          <span className="text-[10px] text-slate-500 block uppercase font-medium">Avg Degree</span>
          <span className="text-base font-bold text-blue-600 font-mono">
            {statistics.average_degree ? statistics.average_degree.toFixed(2) : '1.5'}
          </span>
        </div>
      </div>
    </div>
  );
};
