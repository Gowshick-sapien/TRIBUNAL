import React from 'react';

export const GraphLegend: React.FC = () => {
  return (
    <div className="surface-card p-3 rounded-lg border border-slate-200 text-xs font-sans space-y-2 shadow-xs bg-white max-w-xs">
      <div className="text-slate-500 font-semibold uppercase tracking-wider text-[10px] border-b border-slate-200 pb-1">
        Evidence Graph Legend
      </div>

      <div className="space-y-1.5 text-slate-700">
        <div className="flex items-center gap-2">
          <span className="w-3 h-3 rounded bg-blue-50 border border-blue-300" />
          <span>Financial Expert Card</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-3 h-3 rounded bg-slate-100 border border-slate-300" />
          <span>Behaviour Expert Card</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-3 h-3 rounded bg-emerald-50 border border-emerald-300" />
          <span>Adversarial Defense Review</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-3 h-3 rounded bg-blue-600 border border-blue-700" />
          <span className="text-blue-700 font-semibold">Tribunal Verdict</span>
        </div>
      </div>

      <div className="border-t border-slate-200 pt-1.5 space-y-1 text-[10px]">
        <div className="flex items-center gap-2">
          <span className="w-4 h-0.5 bg-emerald-600" />
          <span className="text-emerald-700 font-medium">Support Edge</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-4 h-0.5 bg-rose-600" />
          <span className="text-rose-700 font-medium">Contradiction Edge</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-4 h-0.5 bg-blue-600" />
          <span className="text-blue-700 font-semibold">Winning Chain Edge</span>
        </div>
      </div>
    </div>
  );
};
