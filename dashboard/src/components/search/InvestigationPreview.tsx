import React, { useEffect, useState } from 'react';
import { X, FileText, Layers, Sparkles } from 'lucide-react';
import type { SearchResultItem } from '../../types/search';
import { RiskChip } from '../common/RiskChip';
import { ConfidenceMeter } from '../common/ConfidenceMeter';
import { searchApi } from '../../services/search_api';

interface InvestigationPreviewProps {
  item: SearchResultItem | null;
  onClose: () => void;
  onNavigateViewer: (id: string) => void;
  onNavigateGraph: (id: string) => void;
}

export const InvestigationPreview: React.FC<InvestigationPreviewProps> = ({
  item,
  onClose,
  onNavigateViewer,
  onNavigateGraph,
}) => {
  const [similarItems, setSimilarItems] = useState<any[]>([]);

  useEffect(() => {
    if (!item) return;
    searchApi.getSimilar(item.id, 3).then((res) => {
      setSimilarItems(res.similar || []);
    }).catch(() => setSimilarItems([]));
  }, [item]);

  if (!item) return null;

  return (
    <div className="fixed inset-y-0 right-0 w-full sm:w-[480px] z-50 glass-panel border-l border-slate-800 p-6 overflow-y-auto space-y-6 shadow-2xl animate-slideInRight backdrop-blur-xl">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-xs font-mono text-cyan-400 font-bold">{item.id}</span>
            <RiskChip risk={item.risk_level} />
          </div>
          <p className="text-xs text-slate-400 font-mono mt-1">
            Executed on {new Date(item.created_at).toLocaleString()}
          </p>
        </div>
        <button
          onClick={onClose}
          className="p-1.5 rounded-lg bg-slate-900 text-slate-400 hover:text-slate-200 transition"
        >
          <X className="w-5 h-5" />
        </button>
      </div>

      {/* Query & Intent */}
      <div className="space-y-3">
        <div className="text-xs font-mono font-bold text-slate-400 uppercase tracking-wider">
          Query & Target Intent
        </div>
        <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1">
          <p className="text-sm font-bold text-slate-100 font-sans">{item.query}</p>
          <div className="text-xs font-mono text-cyan-400">Planner Intent: {item.planner_intent}</div>
        </div>
      </div>

      {/* Primary Winning Hypothesis & Metrics */}
      <div className="space-y-3">
        <div className="text-xs font-mono font-bold text-slate-400 uppercase tracking-wider">
          Winning Hypothesis & Confidence
        </div>
        <div className="glass-card p-4 rounded-xl border border-slate-800 space-y-3">
          <p className="text-sm font-bold text-slate-200 font-sans">
            {item.winning_hypothesis || 'Multi-Pattern Laundry Finding'}
          </p>
          <ConfidenceMeter confidence={item.confidence} />
        </div>
      </div>

      {/* Recommendation */}
      <div className="space-y-2">
        <div className="text-xs font-mono font-bold text-slate-400 uppercase tracking-wider">
          Tribunal Recommendation
        </div>
        <p className="text-xs font-mono text-slate-300 bg-slate-900/60 p-3 rounded-lg border border-slate-800 leading-relaxed">
          {item.recommendation}
        </p>
      </div>

      {/* Topology Stats */}
      <div className="grid grid-cols-2 gap-3 text-xs font-mono">
        <div className="p-3 rounded-lg bg-slate-900/60 border border-slate-800">
          <span className="text-[10px] text-slate-500 block">Graph Topology</span>
          <span className="text-cyan-400 font-bold">{item.node_count} Nodes / {item.edge_count} Edges</span>
        </div>
        <div className="p-3 rounded-lg bg-slate-900/60 border border-slate-800">
          <span className="text-[10px] text-slate-500 block">Execution Latency</span>
          <span className="text-cyan-400 font-bold">{item.duration_ms.toFixed(1)} ms</span>
        </div>
      </div>

      {/* Similar Investigations Discovery */}
      {similarItems.length > 0 && (
        <div className="space-y-2 border-t border-slate-800 pt-4">
          <div className="text-xs font-mono font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
            <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
            Similar Investigations (Ranked by Metadata)
          </div>
          <div className="space-y-2">
            {similarItems.map((s, idx) => (
              <div
                key={idx}
                onClick={() => onNavigateViewer(s.item.id)}
                className="p-3 rounded-xl bg-slate-900/80 border border-slate-800 hover:border-cyan-500/50 cursor-pointer transition space-y-1"
              >
                <div className="flex items-center justify-between text-xs font-mono">
                  <span className="font-bold text-cyan-400">{s.item.id}</span>
                  <span className="px-2 py-0.5 rounded bg-cyan-950 text-cyan-300 border border-cyan-800 font-bold">
                    {(s.similarity_score * 100).toFixed(0)}% Similar
                  </span>
                </div>
                <p className="text-xs text-slate-300 font-sans truncate">{s.item.query}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Quick Workstation Navigation Buttons */}
      <div className="pt-4 border-t border-slate-800 flex flex-col gap-2 font-mono text-xs">
        <button
          onClick={() => onNavigateViewer(item.id)}
          className="w-full py-2.5 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold transition flex items-center justify-center gap-2"
        >
          <FileText className="w-4 h-4" />
          Open Full Investigation Viewer
        </button>
        <button
          onClick={() => onNavigateGraph(item.id)}
          className="w-full py-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-700 font-bold transition flex items-center justify-center gap-2"
        >
          <Layers className="w-4 h-4 text-cyan-400" />
          Open Interactive Graph Studio (D.4)
        </button>
      </div>
    </div>
  );
};
