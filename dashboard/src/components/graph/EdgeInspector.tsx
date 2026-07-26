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
    <div className="w-80 bg-white h-full border-l border-slate-200 p-5 overflow-y-auto space-y-6 font-sans text-xs shadow-lg">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-200 pb-3">
        <div className="flex items-center gap-2">
          <Share2 className="w-4 h-4 text-blue-600" />
          <h3 className="font-sans text-xs font-semibold text-slate-900 uppercase tracking-wider">
            Edge Relationship Inspector
          </h3>
        </div>
        <button
          onClick={onClose}
          className="p-1 rounded-md bg-white border border-slate-200 text-slate-500 hover:text-slate-900 hover:bg-slate-50 transition-colors"
        >
          <X className="w-4 h-4" />
        </button>
      </div>

      {/* Relationship Type */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <span
            className={`px-2.5 py-0.5 rounded-full text-xs font-mono font-medium border uppercase tracking-wider ${
              isSupport
                ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                : isContradiction
                ? 'bg-rose-50 text-rose-700 border-rose-200'
                : 'bg-blue-50 text-blue-700 border-blue-200'
            }`}
          >
            {edge.relation} RELATION
          </span>
          <span className="text-xs font-mono text-slate-900 font-semibold">
            Weight: {edge.weight.toFixed(2)}
          </span>
        </div>

        <div className="surface-card p-4 rounded-lg border border-slate-200 space-y-2 text-xs font-sans">
          <div>
            <span className="text-slate-500 block text-[10px]">Source Node:</span>
            <span className="font-mono font-semibold text-slate-900">{edge.source}</span>
          </div>
          <div>
            <span className="text-slate-500 block text-[10px]">Target Node:</span>
            <span className="font-mono font-semibold text-slate-900">{edge.target}</span>
          </div>
        </div>
      </div>

      {/* Reasoning Description */}
      <div className="space-y-2">
        <div className="text-[11px] font-sans font-semibold text-slate-500 uppercase tracking-wider">
          Support / Contradiction Reasoning
        </div>
        <p className="text-xs font-sans text-slate-800 bg-slate-50 p-3.5 rounded-lg border border-slate-200 leading-relaxed">
          {edge.reasoning || `Edge ${edge.relation} connects ${edge.source} to ${edge.target} with weight ${edge.weight}.`}
        </p>
      </div>

      {/* Provenance Author */}
      <div className="text-xs font-sans text-slate-500 pt-3 border-t border-slate-200 flex justify-between">
        <span>Created By:</span>
        <span className="text-blue-600 font-mono font-semibold">{edge.created_by || 'EvidenceGraphBuilder'}</span>
      </div>
    </div>
  );
};
