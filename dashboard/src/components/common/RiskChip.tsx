import React from 'react';

interface RiskChipProps {
  risk: string;
}

export const RiskChip: React.FC<RiskChipProps> = ({ risk }) => {
  const getStyle = () => {
    switch ((risk || '').toUpperCase()) {
      case 'CRITICAL':
        return 'bg-rose-50 text-rose-700 border-rose-200';
      case 'HIGH':
        return 'bg-rose-50 text-rose-700 border-rose-200';
      case 'MEDIUM':
        return 'bg-amber-50 text-amber-700 border-amber-200';
      case 'LOW':
        return 'bg-emerald-50 text-emerald-700 border-emerald-200';
      default:
        return 'bg-slate-100 text-slate-700 border-slate-200';
    }
  };

  return (
    <span
      className={`px-2 py-0.5 rounded text-[11px] font-mono font-medium border uppercase tracking-wider inline-flex items-center gap-1 ${getStyle()}`}
    >
      {risk || 'LOW'} RISK
    </span>
  );
};
