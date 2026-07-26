import React, { memo } from 'react';
import { Handle, Position } from '@xyflow/react';
import { Scale } from 'lucide-react';
import type { GraphNodeData } from '../../../types/graph';

interface DefenseNodeProps {
  data: GraphNodeData;
  selected?: boolean;
}

export const DefenseNode: React.FC<DefenseNodeProps> = memo(({ data, selected }) => {
  return (
    <div
      className={`w-64 bg-white rounded-lg p-3.5 border border-emerald-300 shadow-xs transition-colors ${
        selected ? 'ring-2 ring-emerald-500' : ''
      } ${data.isDimmed ? 'opacity-30' : 'opacity-100'}`}
    >
      <Handle type="target" position={Position.Left} className="w-2.5 h-2.5 bg-emerald-600 border-2 border-white" />

      <div className="flex items-center justify-between mb-2">
        <span className="inline-flex items-center gap-1 text-[10px] font-sans font-semibold px-2 py-0.5 rounded bg-emerald-50 border border-emerald-200 text-emerald-700 uppercase tracking-wider">
          <Scale className="w-3 h-3 text-emerald-600" />
          Adversarial Defense
        </span>
        <span className="text-[10px] font-mono text-emerald-700 font-semibold bg-emerald-50 px-1.5 py-0.5 rounded border border-emerald-200">
          Rebuttal
        </span>
      </div>

      <div className="font-sans font-semibold text-xs text-slate-900 line-clamp-2 leading-tight mb-2">
        {data.counter_hypothesis || data.hypothesis || 'Legitimate Business Counter-Explanation'}
      </div>

      <div className="text-[10px] font-sans text-slate-500 pt-2 border-t border-slate-200">
        Status: <span className="text-emerald-700 font-mono font-semibold">{data.rebuttal_status || 'Reviewed'}</span>
      </div>

      <Handle type="source" position={Position.Right} className="w-2.5 h-2.5 bg-emerald-600 border-2 border-white" />
    </div>
  );
});

DefenseNode.displayName = 'DefenseNode';
