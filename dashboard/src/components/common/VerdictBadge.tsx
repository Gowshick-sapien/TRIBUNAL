import React from 'react';
import { AlertTriangle, CheckCircle, ShieldAlert, HelpCircle } from 'lucide-react';

interface VerdictBadgeProps {
  verdict: string;
  size?: 'sm' | 'md' | 'lg';
}

export const VerdictBadge: React.FC<VerdictBadgeProps> = ({ verdict, size = 'md' }) => {
  const getStyles = () => {
    switch (verdict.toUpperCase()) {
      case 'LIKELY_MALICIOUS':
        return {
          bg: 'bg-rose-500/15 border-rose-500/30 text-rose-400',
          icon: ShieldAlert,
          label: 'LIKELY MALICIOUS',
        };
      case 'POSSIBLY_MALICIOUS':
        return {
          bg: 'bg-amber-500/15 border-amber-500/30 text-amber-400',
          icon: AlertTriangle,
          label: 'POSSIBLY MALICIOUS',
        };
      case 'LIKELY_LEGITIMATE':
        return {
          bg: 'bg-emerald-500/15 border-emerald-500/30 text-emerald-400',
          icon: CheckCircle,
          label: 'LIKELY LEGITIMATE',
        };
      default:
        return {
          bg: 'bg-slate-500/15 border-slate-500/30 text-slate-400',
          icon: HelpCircle,
          label: verdict || 'INCONCLUSIVE',
        };
    }
  };

  const style = getStyles();
  const Icon = style.icon;

  const sizeClasses = {
    sm: 'px-2 py-0.5 text-xs gap-1',
    md: 'px-3 py-1 text-sm gap-1.5',
    lg: 'px-4 py-1.5 text-base gap-2 font-bold',
  };

  return (
    <span
      className={`inline-flex items-center rounded-full border font-mono tracking-wide ${style.bg} ${sizeClasses[size]}`}
    >
      <Icon className={size === 'sm' ? 'w-3.5 h-3.5' : size === 'lg' ? 'w-5 h-5' : 'w-4 h-4'} />
      {style.label}
    </span>
  );
};
