import React from 'react';

export const GraphLegend: React.FC = () => {
  return (
    <div className="glass-panel p-3 rounded-xl border border-slate-800 text-[11px] font-mono space-y-2 shadow-lg max-w-xs">
      <div className="text-slate-400 font-bold uppercase tracking-wider text-[10px] border-b border-slate-800 pb-1">
        Evidence Graph Legend
      </div>

      <div className="space-y-1.5">
        <div className="flex items-center gap-2">
          <span className="w-3 h-3 rounded bg-cyan-950 border border-cyan-500" />
          <span className="text-slate-300">Financial Expert Card</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-3 h-3 rounded bg-purple-950 border border-purple-500" />
          <span className="text-slate-300">Behaviour Expert Card</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-3 h-3 rounded bg-emerald-950 border border-emerald-500" />
          <span className="text-slate-300">Adversarial Defense Review</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-3 h-3 rounded bg-cyan-500 border border-cyan-300" />
          <span className="text-cyan-300 font-bold">Tribunal Verdict</span>
        </div>
      </div>

      <div className="border-t border-slate-800 pt-1.5 space-y-1 text-[10px]">
        <div className="flex items-center gap-2">
          <span className="w-4 h-0.5 bg-emerald-400" />
          <span className="text-emerald-400">Support Edge</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-4 h-0.5 bg-rose-500" />
          <span className="text-rose-400">Contradiction Edge</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-4 h-0.5 bg-cyan-400 shadow-sm shadow-cyan-400" />
          <span className="text-cyan-300 font-bold">Winning Chain Edge</span>
        </div>
      </div>
    </div>
  );
};
