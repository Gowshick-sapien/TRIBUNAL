import React, { memo } from 'react';
import { Handle, Position } from '@xyflow/react';
import { HelpCircle } from 'lucide-react';
import type { GraphNodeData } from '../../../types/graph';

interface EvidenceGapNodeProps {
  data: GraphNodeData;
  selected?: boolean;
}

export const EvidenceGapNode: React.FC<EvidenceGapNodeProps> = memo(({ data, selected }) => {
  return (
    <div
      className={`w-60 glass-panel rounded-xl p-3.5 border border-dashed border-amber-500/70 bg-amber-950/20 transition-all duration-300 ${
        selected ? 'ring-2 ring-amber-400 scale-[1.02]' : ''
      } ${data.isDimmed ? 'opacity-30' : 'opacity-100'}`}
    >
      <Handle type="target" position={Position.Left} className="w-2.5 h-2.5 bg-amber-400 border-2 border-slate-900" />

      <div className="flex items-center justify-between mb-2">
        <span className="inline-flex items-center gap-1 text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-amber-950/80 border border-amber-800 text-amber-300 uppercase tracking-wider">
          <HelpCircle className="w-3 h-3 text-amber-400" />
          Missing Evidence
        </span>
        <span className="text-[10px] font-mono text-amber-400 font-bold">GAP</span>
      </div>

      <div className="font-sans font-bold text-xs text-slate-200 line-clamp-2 leading-tight mb-2">
        {data.label || 'Requested Data Unavailable'}
      </div>

      <div className="text-[10px] font-mono text-slate-400 pt-2 border-t border-slate-800">
        Type: <span className="text-amber-300">{data.missing_data_type || 'Unlinked Counterparty Records'}</span>
      </div>

      <Handle type="source" position={Position.Right} className="w-2.5 h-2.5 bg-amber-400 border-2 border-slate-900" />
    </div>
  );
});

EvidenceGapNode.displayName = 'EvidenceGapNode';
