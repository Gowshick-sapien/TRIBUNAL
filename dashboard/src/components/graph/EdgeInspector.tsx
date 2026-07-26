import React from 'react';
import { X, Share2 } from 'lucide-react';
import type { GraphEdgeData } from '../../types/graph';

interface EdgeInspectorProps {
  edge: GraphEdgeData | null;
  onClose: () => void;
}

export const EdgeInspector: React.FC<EdgeInspectorProps> = ({ edge, onClose }) => {
  if (!edge) return null;

  const isSupport = edge.relation === 'SUPPORT';
  const isContradiction = edge.relation === 'CONTRADICTION';

  return (
    <div className="w-80 glass-panel h-full border-l border-slate-800 p-5 overflow-y-auto space-y-6 animate-slideInRight">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center gap-2">
          <Share2 className="w-4 h-4 text-cyan-400" />
          <h3 className="font-mono text-xs font-bold text-slate-200 uppercase tracking-wider">
            Edge Relationship Inspector
          </h3>
        </div>
        <button
          onClick={onClose}
          className="p-1 rounded bg-slate-900 text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition"
        >
          <X className="w-4 h-4" />
        </button>
      </div>

      {/* Relationship Type */}
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <span
            className={`px-3 py-1 rounded-full text-xs font-mono font-bold border uppercase tracking-wider ${
              isSupport
                ? 'bg-emerald-950/80 text-emerald-300 border-emerald-800'
                : isContradiction
                ? 'bg-rose-950/80 text-rose-300 border-rose-800'
                : 'bg-cyan-950/80 text-cyan-300 border-cyan-800'
            }`}
          >
            {edge.relation} RELATION
          </span>
          <span className="text-xs font-mono text-cyan-400 font-bold">
            Weight: {edge.weight.toFixed(2)}
          </span>
        </div>

        <div className="glass-card p-4 rounded-xl border border-slate-800 space-y-2 text-xs font-mono">
          <div>
            <span className="text-slate-500 block text-[10px]">Source Node:</span>
            <span className="font-bold text-slate-200">{edge.source}</span>
          </div>
          <div>
            <span className="text-slate-500 block text-[10px]">Target Node:</span>
            <span className="font-bold text-slate-200">{edge.target}</span>
          </div>
        </div>
      </div>

      {/* Reasoning Description */}
      <div className="space-y-2">
        <div className="text-[11px] font-mono font-bold text-slate-400 uppercase tracking-wider">
          Support / Contradiction Reasoning
        </div>
        <p className="text-xs font-sans text-slate-200 bg-slate-900 p-3.5 rounded-xl border border-slate-800 leading-relaxed">
          {edge.reasoning || `Edge ${edge.relation} connects ${edge.source} to ${edge.target} with weight ${edge.weight}.`}
        </p>
      </div>

      {/* Provenance Author */}
      <div className="text-xs font-mono text-slate-400 pt-3 border-t border-slate-800 flex justify-between">
        <span>Created By:</span>
        <span className="text-cyan-400 font-bold">{edge.created_by || 'EvidenceGraphBuilder'}</span>
      </div>
    </div>
  );
};
