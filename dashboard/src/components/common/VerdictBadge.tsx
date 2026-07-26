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
          bg: 'bg-rose-50 border-rose-200 text-rose-700',
          icon: ShieldAlert,
          label: 'LIKELY MALICIOUS',
        };
      case 'POSSIBLY_MALICIOUS':
        return {
          bg: 'bg-amber-50 border-amber-200 text-amber-700',
          icon: AlertTriangle,
          label: 'POSSIBLY MALICIOUS',
        };
      case 'LIKELY_LEGITIMATE':
        return {
          bg: 'bg-emerald-50 border-emerald-200 text-emerald-700',
          icon: CheckCircle,
          label: 'LIKELY LEGITIMATE',
        };
      default:
        return {
          bg: 'bg-slate-100 border-slate-200 text-slate-700',
          icon: HelpCircle,
          label: verdict || 'INCONCLUSIVE',
        };
    }
  };

  const style = getStyles();
  const Icon = style.icon;

  const sizeClasses = {
    sm: 'px-2 py-0.5 text-xs gap-1',
    md: 'px-2.5 py-1 text-xs gap-1.5 font-medium',
    lg: 'px-3.5 py-1.5 text-sm gap-2 font-semibold',
  };

  return (
    <span
      className={`inline-flex items-center rounded-md border font-sans tracking-tight ${style.bg} ${sizeClasses[size]}`}
    >
      <Icon className={size === 'sm' ? 'w-3.5 h-3.5' : size === 'lg' ? 'w-4.5 h-4.5' : 'w-4 h-4'} />
      {style.label}
    </span>
  );
};
