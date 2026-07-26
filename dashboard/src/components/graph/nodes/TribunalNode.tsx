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
      className={`w-72 glass-panel rounded-2xl p-4 border border-cyan-400/80 bg-gradient-to-br from-cyan-950/60 to-slate-900 shadow-xl shadow-cyan-500/20 transition-all duration-300 ${
        selected ? 'ring-4 ring-cyan-400 scale-[1.03]' : ''
      } ${data.isDimmed ? 'opacity-30' : 'opacity-100'}`}
    >
      <Handle type="target" position={Position.Left} className="w-3 h-3 bg-cyan-400 border-2 border-slate-900" />

      <div className="flex items-center justify-between mb-2">
        <span className="inline-flex items-center gap-1.5 text-[11px] font-mono font-black text-cyan-300 bg-cyan-950 px-2.5 py-1 rounded-full border border-cyan-800 tracking-wider">
          <Award className="w-3.5 h-3.5 text-cyan-400" />
          TRIBUNAL CONSENSUS
        </span>
        <span className="text-xs font-mono font-black text-cyan-300 bg-slate-950 px-2 py-0.5 rounded border border-cyan-900">
          {confidence}% CONFIDENCE
        </span>
      </div>

      <div className="font-sans font-black text-sm text-slate-100 mb-2 leading-snug">
        {data.hypothesis || 'Consensus Verdict Reached'}
      </div>

      <div className="text-[11px] font-mono text-cyan-200/90 bg-slate-950/80 p-2.5 rounded-lg border border-cyan-900/60">
        Primary Winning Hypothesis Selected by Multi-Expert Tribunal
      </div>

      <Handle type="source" position={Position.Right} className="w-3 h-3 bg-cyan-400 border-2 border-slate-900" />
    </div>
  );
});

TribunalNode.displayName = 'TribunalNode';
