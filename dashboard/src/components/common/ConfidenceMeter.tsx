import React from 'react';

interface ConfidenceMeterProps {
  confidence: number; // 0.0 to 1.0
  showLabel?: boolean;
}

export const ConfidenceMeter: React.FC<ConfidenceMeterProps> = ({ confidence, showLabel = true }) => {
  const percentage = Math.round((confidence || 0) * 100);

  const getColor = () => {
    if (percentage >= 80) return 'bg-blue-600';
    if (percentage >= 50) return 'bg-amber-600';
    return 'bg-slate-500';
  };

  return (
    <div className="w-full space-y-1">
      {showLabel && (
        <div className="flex justify-between items-center text-xs font-sans">
          <span className="text-slate-500">Calibrated Confidence</span>
          <span className="text-slate-900 font-semibold font-mono">{percentage}%</span>
        </div>
      )}
      <div className="w-full h-2 bg-slate-100 rounded-full overflow-hidden border border-slate-200">
        <div
          className={`h-full rounded-full ${getColor()} transition-all duration-500 ease-out`}
          style={{ width: `${Math.min(100, Math.max(0, percentage))}%` }}
        />
      </div>
    </div>
  );
};
