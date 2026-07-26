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
    <div className="w-80 bg-white h-full border-l border-slate-200 p-5 overflow-y-auto space-y-6 font-sans text-xs shadow-lg">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-200 pb-3">
        <div className="flex items-center gap-2">
          <FileText className="w-4 h-4 text-blue-600" />
          <h3 className="font-sans text-xs font-semibold text-slate-900 uppercase tracking-wider">
            Node Inspector
          </h3>
        </div>
        <button
          onClick={onClose}
          className="p-1 rounded-md bg-white border border-slate-200 text-slate-500 hover:text-slate-900 hover:bg-slate-50 transition-colors"
        >
          <X className="w-4 h-4" />
        </button>
      </div>

      {/* Node Identity Card */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <span className="font-mono text-xs font-semibold text-blue-600">{node.id}</span>
          {node.severity && <RiskChip risk={node.severity} />}
        </div>

        <h2 className="font-sans font-bold text-sm text-slate-900 leading-snug">
          {node.hypothesis || node.label}
        </h2>

        {node.confidence !== undefined && (
          <div className="pt-1">
            <ConfidenceMeter confidence={node.confidence} />
          </div>
        )}
      </div>

      {/* Metadata Overview */}
      <div className="surface-card p-4 rounded-lg border border-slate-200 space-y-2.5 text-xs font-sans">
        <div className="flex justify-between">
          <span className="text-slate-500">Node Type</span>
          <span className="text-slate-900 uppercase font-semibold font-mono">{node.type}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-slate-500">Source Expert</span>
          <span className="text-blue-600 font-semibold capitalize">{node.expert || 'Domain Expert'}</span>
        </div>
        {node.generated_at && (
          <div className="flex justify-between">
            <span className="text-slate-500">Generated</span>
            <span className="text-slate-700 font-mono">{new Date(node.generated_at).toLocaleTimeString()}</span>
          </div>
        )}
        {node.rebuttal_status && (
          <div className="flex justify-between">
            <span className="text-slate-500">Rebuttal Status</span>
            <span className="text-emerald-700 font-semibold">{node.rebuttal_status}</span>
          </div>
        )}
      </div>

      {/* Counter Hypothesis (if defense node) */}
      {node.counter_hypothesis && (
        <div className="space-y-2">
          <div className="text-[11px] font-sans font-semibold text-slate-500 uppercase tracking-wider flex items-center gap-1.5">
            <Scale className="w-3.5 h-3.5 text-emerald-600" />
            Counter-Hypothesis (Defense)
          </div>
          <p className="text-xs font-sans text-slate-800 bg-emerald-50 p-3 rounded-lg border border-emerald-200 leading-relaxed">
            {node.counter_hypothesis}
          </p>
        </div>
      )}

      {/* Evidence Provenance */}
      <div className="space-y-3 border-t border-slate-200 pt-4">
        <div className="text-[11px] font-sans font-semibold text-slate-500 uppercase tracking-wider flex items-center gap-1.5">
          <Database className="w-3.5 h-3.5 text-blue-600" />
          Evidence Provenance & Transactions
        </div>

        {node.transaction_ids && node.transaction_ids.length > 0 ? (
          <div className="space-y-1.5">
            {node.transaction_ids.slice(0, 5).map((tx, idx) => (
              <div key={idx} className="p-2 rounded-md bg-slate-50 border border-slate-200 text-[11px] font-mono text-blue-600 flex items-center justify-between">
                <span>TX: {tx}</span>
                <span className="text-[9px] text-slate-500 font-sans">Verified</span>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-xs text-slate-500 font-sans italic">
            Derived directly from rule execution and graph synthesis.
          </p>
        )}
      </div>
    </div>
  );
};
