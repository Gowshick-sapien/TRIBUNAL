import React, { memo } from 'react';
import { Handle, Position } from '@xyflow/react';
import type { GraphNodeData } from '../../../types/graph';

interface CardNodeProps {
  data: GraphNodeData;
  selected?: boolean;
}

export const CardNode: React.FC<CardNodeProps> = memo(({ data, selected }) => {
  const isFinancial = (data.expert || '').toLowerCase().includes('fin');
  const severity = data.severity || 'MEDIUM';
  const confidence = Math.round((data.confidence || 0.5) * 100);

  const getBorderColor = () => {
    if (data.isWinningPath) return 'border-cyan-400 ring-2 ring-cyan-400/50 shadow-lg shadow-cyan-500/30';
    if (severity === 'CRITICAL') return 'border-rose-500/80 shadow-rose-500/20';
    if (severity === 'HIGH') return 'border-orange-500/80 shadow-orange-500/20';
    return 'border-slate-700 hover:border-cyan-500/50';
  };

  const getBadgeStyle = () => {
    if (isFinancial) return 'bg-cyan-950/80 border-cyan-800 text-cyan-300';
    return 'bg-purple-950/80 border-purple-800 text-purple-300';
  };

  return (
    <div
      className={`w-64 glass-panel rounded-xl p-3.5 border transition-all duration-300 ${getBorderColor()} ${
        selected ? 'ring-2 ring-cyan-400 scale-[1.02]' : ''
      } ${data.isDimmed ? 'opacity-30 blur-[0.5px]' : 'opacity-100'}`}
    >
      <Handle type="target" position={Position.Left} className="w-2.5 h-2.5 bg-cyan-400 border-2 border-slate-900" />

      <div className="flex items-center justify-between gap-2 mb-2">
        <span className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded border uppercase tracking-wider ${getBadgeStyle()}`}>
          {isFinancial ? 'Financial Expert' : 'Behaviour Expert'}
        </span>
        <span className="text-[10px] font-mono text-cyan-400 font-bold bg-slate-900/80 px-1.5 py-0.5 rounded border border-slate-800">
          {confidence}%
        </span>
      </div>

      <div className="font-sans font-bold text-xs text-slate-100 line-clamp-2 leading-tight mb-2">
        {data.hypothesis || data.label}
      </div>

      <div className="flex items-center justify-between text-[10px] font-mono text-slate-400 pt-2 border-t border-slate-800/80">
        <span className="truncate max-w-[120px]">ID: {data.id}</span>
        <span
          className={`font-semibold uppercase ${
            severity === 'CRITICAL'
              ? 'text-rose-400'
              : severity === 'HIGH'
              ? 'text-orange-400'
              : 'text-amber-400'
          }`}
        >
          {severity}
        </span>
      </div>

      <Handle type="source" position={Position.Right} className="w-2.5 h-2.5 bg-cyan-400 border-2 border-slate-900" />
    </div>
  );
});

CardNode.displayName = 'CardNode';
