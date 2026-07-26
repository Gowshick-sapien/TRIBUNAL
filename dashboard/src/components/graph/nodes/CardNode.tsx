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
    if (data.isWinningPath) return 'border-blue-600 ring-2 ring-blue-500/20 shadow-sm';
    if (severity === 'CRITICAL') return 'border-rose-300 shadow-xs';
    if (severity === 'HIGH') return 'border-amber-300 shadow-xs';
    return 'border-slate-200 hover:border-blue-300';
  };

  const getBadgeStyle = () => {
    if (isFinancial) return 'bg-blue-50 border-blue-200 text-blue-700';
    return 'bg-slate-100 border-slate-200 text-slate-700';
  };

  return (
    <div
      className={`w-64 bg-white rounded-lg p-3.5 border transition-colors shadow-xs ${getBorderColor()} ${
        selected ? 'ring-2 ring-blue-500' : ''
      } ${data.isDimmed ? 'opacity-30' : 'opacity-100'}`}
    >
      <Handle type="target" position={Position.Left} className="w-2.5 h-2.5 bg-blue-600 border-2 border-white" />

      <div className="flex items-center justify-between gap-2 mb-2">
        <span className={`text-[10px] font-sans font-semibold px-2 py-0.5 rounded border uppercase tracking-wider ${getBadgeStyle()}`}>
          {isFinancial ? 'Financial Expert' : 'Behaviour Expert'}
        </span>
        <span className="text-[10px] font-mono text-slate-700 font-semibold bg-slate-100 px-1.5 py-0.5 rounded border border-slate-200">
          {confidence}%
        </span>
      </div>

      <div className="font-sans font-semibold text-xs text-slate-900 line-clamp-2 leading-tight mb-2">
        {data.hypothesis || data.label}
      </div>

      <div className="flex items-center justify-between text-[10px] font-sans text-slate-500 pt-2 border-t border-slate-200">
        <span className="truncate max-w-[120px] font-mono">ID: {data.id}</span>
        <span
          className={`font-semibold uppercase font-mono ${
            severity === 'CRITICAL'
              ? 'text-rose-700'
              : severity === 'HIGH'
              ? 'text-amber-700'
              : 'text-slate-700'
          }`}
        >
          {severity}
        </span>
      </div>

      <Handle type="source" position={Position.Right} className="w-2.5 h-2.5 bg-blue-600 border-2 border-white" />
    </div>
  );
});

CardNode.displayName = 'CardNode';
