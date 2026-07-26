import React from 'react';

interface RiskChipProps {
  risk: string;
}

export const RiskChip: React.FC<RiskChipProps> = ({ risk }) => {
  const getStyle = () => {
    switch ((risk || '').toUpperCase()) {
      case 'CRITICAL':
        return 'bg-rose-950/80 text-rose-300 border-rose-600/50';
      case 'HIGH':
        return 'bg-orange-950/80 text-orange-300 border-orange-600/50';
      case 'MEDIUM':
        return 'bg-amber-950/80 text-amber-300 border-amber-600/50';
      default:
        return 'bg-slate-800/80 text-slate-300 border-slate-600/50';
    }
  };

  return (
    <span
      className={`px-2.5 py-0.5 rounded text-xs font-mono font-semibold border uppercase tracking-wider ${getStyle()}`}
    >
      {risk || 'LOW'} RISK
    </span>
  );
};
