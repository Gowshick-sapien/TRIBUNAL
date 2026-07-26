import React from 'react';
import { X, FileText, Database, Scale } from 'lucide-react';
import type { GraphNodeData } from '../../types/graph';
import { RiskChip } from '../common/RiskChip';
import { ConfidenceMeter } from '../common/ConfidenceMeter';

interface NodeInspectorProps {
  node: GraphNodeData | null;
  onClose: () => void;
}

export const NodeInspector: React.FC<NodeInspectorProps> = ({ node, onClose }) => {
  if (!node) return null;

  return (
    <div className="w-80 glass-panel h-full border-l border-slate-800 p-5 overflow-y-auto space-y-6 animate-slideInRight">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center gap-2">
          <FileText className="w-4 h-4 text-cyan-400" />
          <h3 className="font-mono text-xs font-bold text-slate-200 uppercase tracking-wider">
            Node Inspector
          </h3>
        </div>
        <button
          onClick={onClose}
          className="p-1 rounded bg-slate-900 text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition"
        >
          <X className="w-4 h-4" />
        </button>
      </div>

      {/* Node Identity Card */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <span className="font-mono text-xs font-bold text-cyan-400">{node.id}</span>
          {node.severity && <RiskChip risk={node.severity} />}
        </div>

        <h2 className="font-sans font-bold text-sm text-slate-100 leading-snug">
          {node.hypothesis || node.label}
        </h2>

        {node.confidence !== undefined && (
          <div className="pt-1">
            <ConfidenceMeter confidence={node.confidence} />
          </div>
        )}
      </div>

      {/* Metadata Overview */}
      <div className="glass-card p-4 rounded-xl border border-slate-800 space-y-2.5 text-xs font-mono">
        <div className="flex justify-between">
          <span className="text-slate-400">Node Type</span>
          <span className="text-slate-200 uppercase font-bold">{node.type}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-slate-400">Source Expert</span>
          <span className="text-cyan-400 font-bold capitalize">{node.expert || 'Domain Expert'}</span>
        </div>
        {node.generated_at && (
          <div className="flex justify-between">
            <span className="text-slate-400">Generated</span>
            <span className="text-slate-300">{new Date(node.generated_at).toLocaleTimeString()}</span>
          </div>
        )}
        {node.rebuttal_status && (
          <div className="flex justify-between">
            <span className="text-slate-400">Rebuttal Status</span>
            <span className="text-emerald-400 font-bold">{node.rebuttal_status}</span>
          </div>
        )}
      </div>

      {/* Counter Hypothesis (if defense node) */}
      {node.counter_hypothesis && (
        <div className="space-y-2">
          <div className="text-[11px] font-mono font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
            <Scale className="w-3.5 h-3.5 text-emerald-400" />
            Counter-Hypothesis (Defense)
          </div>
          <p className="text-xs font-sans text-emerald-300 bg-emerald-950/40 p-3 rounded-lg border border-emerald-800/50 leading-relaxed">
            {node.counter_hypothesis}
          </p>
        </div>
      )}

      {/* Evidence Provenance */}
      <div className="space-y-3 border-t border-slate-800 pt-4">
        <div className="text-[11px] font-mono font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
          <Database className="w-3.5 h-3.5 text-cyan-400" />
          Evidence Provenance & Transactions
        </div>

        {node.transaction_ids && node.transaction_ids.length > 0 ? (
          <div className="space-y-1.5">
            {node.transaction_ids.slice(0, 5).map((tx, idx) => (
              <div key={idx} className="p-2 rounded bg-slate-900 border border-slate-800 text-[11px] font-mono text-cyan-300 flex items-center justify-between">
                <span>TX: {tx}</span>
                <span className="text-[9px] text-slate-500">Verified</span>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-xs text-slate-500 font-mono italic">
            Derived directly from rule execution and graph synthesis.
          </p>
        )}
      </div>
    </div>
  );
};
