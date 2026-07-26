import React from 'react';

interface ConfidenceMeterProps {
  confidence: number; // 0.0 to 1.0
  showLabel?: boolean;
}

export const ConfidenceMeter: React.FC<ConfidenceMeterProps> = ({ confidence, showLabel = true }) => {
  const percentage = Math.round((confidence || 0) * 100);

  const getColor = () => {
    if (percentage >= 80) return 'from-cyan-500 to-emerald-400';
    if (percentage >= 50) return 'from-amber-500 to-yellow-400';
    return 'from-slate-500 to-slate-400';
  };

  return (
    <div className="w-full">
      {showLabel && (
        <div className="flex justify-between items-center text-xs font-mono mb-1.5">
          <span className="text-slate-400">Calibrated Confidence</span>
          <span className="text-cyan-400 font-bold">{percentage}%</span>
        </div>
      )}
      <div className="w-full h-2 bg-slate-900 rounded-full overflow-hidden border border-slate-800 p-0.5">
        <div
          className={`h-full rounded-full bg-gradient-to-r ${getColor()} transition-all duration-700 ease-out`}
          style={{ width: `${Math.min(100, Math.max(0, percentage))}%` }}
        />
      </div>
    </div>
  );
};
