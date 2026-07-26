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
      className={`w-60 bg-amber-50/50 rounded-lg p-3.5 border border-dashed border-amber-300 shadow-xs transition-colors ${
        selected ? 'ring-2 ring-amber-500' : ''
      } ${data.isDimmed ? 'opacity-30' : 'opacity-100'}`}
    >
      <Handle type="target" position={Position.Left} className="w-2.5 h-2.5 bg-amber-600 border-2 border-white" />

      <div className="flex items-center justify-between mb-2">
        <span className="inline-flex items-center gap-1 text-[10px] font-sans font-semibold px-2 py-0.5 rounded bg-amber-100 border border-amber-200 text-amber-800 uppercase tracking-wider">
          <HelpCircle className="w-3 h-3 text-amber-700" />
          Missing Evidence
        </span>
        <span className="text-[10px] font-mono text-amber-700 font-semibold">GAP</span>
      </div>

      <div className="font-sans font-semibold text-xs text-slate-900 line-clamp-2 leading-tight mb-2">
        {data.label || 'Requested Data Unavailable'}
      </div>

      <div className="text-[10px] font-sans text-slate-600 pt-2 border-t border-amber-200">
        Type: <span className="text-amber-800 font-mono font-semibold">{data.missing_data_type || 'Unlinked Counterparty Records'}</span>
      </div>

      <Handle type="source" position={Position.Right} className="w-2.5 h-2.5 bg-amber-600 border-2 border-white" />
    </div>
  );
});

EvidenceGapNode.displayName = 'EvidenceGapNode';
