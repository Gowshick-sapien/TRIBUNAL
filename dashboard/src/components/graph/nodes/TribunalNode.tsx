import React, { memo } from 'react';
import { Handle, Position } from '@xyflow/react';
import { Award } from 'lucide-react';
import type { GraphNodeData } from '../../../types/graph';

interface TribunalNodeProps {
  data: GraphNodeData;
  selected?: boolean;
}

export const TribunalNode: React.FC<TribunalNodeProps> = memo(({ data, selected }) => {
  const confidence = Math.round((data.confidence || 0.9) * 100);

  return (
    <div
      className={`w-72 bg-white rounded-lg p-4 border-2 border-blue-600 shadow-sm transition-colors ${
        selected ? 'ring-2 ring-blue-500' : ''
      } ${data.isDimmed ? 'opacity-30' : 'opacity-100'}`}
    >
      <Handle type="target" position={Position.Left} className="w-3 h-3 bg-blue-600 border-2 border-white" />

      <div className="flex items-center justify-between mb-2">
        <span className="inline-flex items-center gap-1.5 text-[11px] font-sans font-semibold text-blue-700 bg-blue-50 px-2.5 py-0.5 rounded border border-blue-200 tracking-wider uppercase">
          <Award className="w-3.5 h-3.5 text-blue-600" />
          TRIBUNAL CONSENSUS
        </span>
        <span className="text-xs font-mono font-semibold text-slate-900 bg-slate-100 px-2 py-0.5 rounded border border-slate-200">
          {confidence}% CONFIDENCE
        </span>
      </div>

      <div className="font-sans font-bold text-sm text-slate-900 mb-2 leading-snug">
        {data.hypothesis || 'Consensus Verdict Reached'}
      </div>

      <div className="text-[11px] font-sans text-slate-700 bg-slate-50 p-2.5 rounded-md border border-slate-200 leading-relaxed">
        Primary Winning Hypothesis Selected by Multi-Expert Tribunal
      </div>

      <Handle type="source" position={Position.Right} className="w-3 h-3 bg-blue-600 border-2 border-white" />
    </div>
  );
});

TribunalNode.displayName = 'TribunalNode';
