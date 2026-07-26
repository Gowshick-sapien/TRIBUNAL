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
    <div className="fixed inset-y-0 right-0 w-full sm:w-[480px] z-50 bg-white border-l border-slate-200 p-6 overflow-y-auto space-y-6 shadow-2xl font-sans">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-200 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-xs font-mono text-blue-600 font-semibold">{item.id}</span>
            <RiskChip risk={item.risk_level} />
          </div>
          <p className="text-xs text-slate-500 font-sans mt-1">
            Executed on {new Date(item.created_at).toLocaleString()}
          </p>
        </div>
        <button
          onClick={onClose}
          className="p-1.5 rounded-md bg-white border border-slate-200 text-slate-500 hover:text-slate-900 hover:bg-slate-50 transition-colors"
        >
          <X className="w-4 h-4" />
        </button>
      </div>

      {/* Query & Intent */}
      <div className="space-y-2">
        <div className="text-[10px] font-sans font-semibold text-slate-500 uppercase tracking-wider">
          Query & Target Intent
        </div>
        <div className="p-3.5 rounded-lg bg-slate-50 border border-slate-200 space-y-1">
          <p className="text-sm font-semibold text-slate-900 font-sans">{item.query}</p>
          <div className="text-xs font-mono text-blue-600 font-medium">Planner Intent: {item.planner_intent}</div>
        </div>
      </div>

      {/* Primary Winning Hypothesis & Metrics */}
      <div className="space-y-2">
        <div className="text-[10px] font-sans font-semibold text-slate-500 uppercase tracking-wider">
          Winning Hypothesis & Confidence
        </div>
        <div className="surface-card p-4 rounded-lg border border-slate-200 space-y-3">
          <p className="text-sm font-semibold text-slate-900 font-sans">
            {item.winning_hypothesis || 'Multi-Pattern Laundry Finding'}
          </p>
          <ConfidenceMeter confidence={item.confidence} />
        </div>
      </div>

      {/* Recommendation */}
      <div className="space-y-2">
        <div className="text-[10px] font-sans font-semibold text-slate-500 uppercase tracking-wider">
          Tribunal Recommendation
        </div>
        <p className="text-xs font-sans text-slate-700 bg-slate-50 p-3 rounded-lg border border-slate-200 leading-relaxed">
          {item.recommendation}
        </p>
      </div>

      {/* Topology Stats */}
      <div className="grid grid-cols-2 gap-3 text-xs font-sans">
        <div className="p-3 rounded-lg bg-slate-50 border border-slate-200">
          <span className="text-[10px] text-slate-500 block uppercase font-medium">Graph Topology</span>
          <span className="text-slate-900 font-semibold font-mono">{item.node_count} Nodes / {item.edge_count} Edges</span>
        </div>
        <div className="p-3 rounded-lg bg-slate-50 border border-slate-200">
          <span className="text-[10px] text-slate-500 block uppercase font-medium">Execution Latency</span>
          <span className="text-slate-900 font-semibold font-mono">{item.duration_ms.toFixed(1)} ms</span>
        </div>
      </div>

      {/* Similar Investigations Discovery */}
      {similarItems.length > 0 && (
        <div className="space-y-2 border-t border-slate-200 pt-4">
          <div className="text-[10px] font-sans font-semibold text-slate-500 uppercase tracking-wider flex items-center gap-1.5">
            <Sparkles className="w-3.5 h-3.5 text-blue-600" />
            Similar Investigations (Ranked by Metadata)
          </div>
          <div className="space-y-2">
            {similarItems.map((s, idx) => (
              <div
                key={idx}
                onClick={() => onNavigateViewer(s.item.id)}
                className="p-3 rounded-lg bg-white border border-slate-200 hover:border-blue-300 hover:bg-slate-50/80 cursor-pointer transition-colors space-y-1 shadow-xs"
              >
                <div className="flex items-center justify-between text-xs font-sans">
                  <span className="font-mono font-semibold text-blue-600">{s.item.id}</span>
                  <span className="px-2 py-0.5 rounded bg-blue-50 text-blue-700 border border-blue-200 font-medium text-[11px]">
                    {(s.similarity_score * 100).toFixed(0)}% Similar
                  </span>
                </div>
                <p className="text-xs text-slate-800 font-sans truncate">{s.item.query}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Quick Workstation Navigation Buttons */}
      <div className="pt-4 border-t border-slate-200 flex flex-col gap-2 font-sans text-xs">
        <button
          onClick={() => onNavigateViewer(item.id)}
          className="w-full py-2 rounded-md bg-blue-600 hover:bg-blue-700 text-white font-medium transition-colors shadow-xs flex items-center justify-center gap-2"
        >
          <FileText className="w-4 h-4" />
          Open Full Investigation Viewer
        </button>
        <button
          onClick={() => onNavigateGraph(item.id)}
          className="w-full py-2 rounded-md bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 font-medium transition-colors shadow-xs flex items-center justify-center gap-2"
        >
          <Layers className="w-4 h-4 text-blue-600" />
          Open Interactive Graph Studio
        </button>
      </div>
    </div>
  );
};
