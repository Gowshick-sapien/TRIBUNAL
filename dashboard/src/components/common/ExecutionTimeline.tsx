import React from 'react';
import { CheckCircle2, Loader2, Circle, Clock } from 'lucide-react';

export interface TimelineStep {
  id: string;
  name: string;
  description: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  durationMs?: number;
}

interface ExecutionTimelineProps {
  steps: TimelineStep[];
  totalMs?: number;
}

export const ExecutionTimeline: React.FC<ExecutionTimelineProps> = ({ steps, totalMs }) => {
  return (
    <div className="w-full glass-panel rounded-xl p-5 border border-slate-800">
      <div className="flex items-center justify-between mb-4 border-b border-slate-800/80 pb-3">
        <h3 className="text-sm font-mono font-semibold text-slate-200 uppercase tracking-wider flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-cyan-400 animate-ping" />
          Engine Execution Pipeline
        </h3>
        {totalMs !== undefined && (
          <span className="text-xs font-mono text-cyan-400 bg-cyan-950/60 border border-cyan-800/50 px-2.5 py-1 rounded flex items-center gap-1.5">
            <Clock className="w-3.5 h-3.5" />
            Total: {totalMs.toFixed(1)} ms
          </span>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-6 gap-3">
        {steps.map((step, idx) => {
          const isCompleted = step.status === 'completed';
          const isRunning = step.status === 'running';

          return (
            <div
              key={step.id}
              className={`p-3 rounded-lg border transition-all duration-300 ${
                isCompleted
                  ? 'bg-emerald-950/20 border-emerald-800/40 text-emerald-300'
                  : isRunning
                  ? 'bg-cyan-950/40 border-cyan-500/60 text-cyan-200 animate-glow'
                  : 'bg-slate-900/40 border-slate-800/60 text-slate-500'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <span className="text-[10px] font-mono uppercase tracking-wider text-slate-400">
                  Step 0{idx + 1}
                </span>
                {isCompleted ? (
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                ) : isRunning ? (
                  <Loader2 className="w-4 h-4 text-cyan-400 animate-spin" />
                ) : (
                  <Circle className="w-4 h-4 text-slate-700" />
                )}
              </div>

              <div className="font-semibold text-xs text-slate-100 truncate mb-1">
                {step.name}
              </div>

              <div className="text-[11px] text-slate-400 line-clamp-2 leading-tight">
                {step.description}
              </div>

              {step.durationMs !== undefined && isCompleted && (
                <div className="mt-2 text-[10px] font-mono text-cyan-400/80 bg-slate-950/60 px-1.5 py-0.5 rounded inline-block">
                  {step.durationMs.toFixed(1)} ms
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};
