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
      className={`w-64 glass-panel rounded-xl p-3.5 border border-emerald-500/60 bg-gradient-to-br from-emerald-950/40 to-slate-900 transition-all duration-300 ${
        selected ? 'ring-2 ring-emerald-400 scale-[1.02]' : ''
      } ${data.isDimmed ? 'opacity-30' : 'opacity-100'}`}
    >
      <Handle type="target" position={Position.Left} className="w-2.5 h-2.5 bg-emerald-400 border-2 border-slate-900" />

      <div className="flex items-center justify-between mb-2">
        <span className="inline-flex items-center gap-1 text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-emerald-950/90 border border-emerald-800 text-emerald-300 uppercase tracking-wider">
          <Scale className="w-3 h-3 text-emerald-400" />
          Adversarial Defense
        </span>
        <span className="text-[10px] font-mono text-emerald-400 font-bold bg-slate-900 px-1.5 py-0.5 rounded border border-slate-800">
          Rebuttal
        </span>
      </div>

      <div className="font-sans font-bold text-xs text-slate-100 line-clamp-2 leading-tight mb-2">
        {data.counter_hypothesis || data.hypothesis || 'Legitimate Business Counter-Explanation'}
      </div>

      <div className="text-[10px] font-mono text-slate-400 pt-2 border-t border-slate-800">
        Status: <span className="text-emerald-300 font-semibold">{data.rebuttal_status || 'Reviewed'}</span>
      </div>

      <Handle type="source" position={Position.Right} className="w-2.5 h-2.5 bg-emerald-400 border-2 border-slate-900" />
    </div>
  );
});

DefenseNode.displayName = 'DefenseNode';
