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
    <div className="w-full surface-card rounded-lg p-5 border border-slate-200">
      <div className="flex items-center justify-between mb-4 border-b border-slate-200 pb-3">
        <h3 className="text-xs font-sans font-semibold text-slate-900 uppercase tracking-wider flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-blue-600" />
          Engine Execution Pipeline
        </h3>
        {totalMs !== undefined && (
          <span className="text-xs font-mono text-slate-700 bg-slate-100 border border-slate-200 px-2.5 py-0.5 rounded-md flex items-center gap-1.5 font-medium">
            <Clock className="w-3.5 h-3.5 text-slate-500" />
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
              className={`p-3 rounded-md border transition-colors ${
                isCompleted
                  ? 'bg-emerald-50/60 border-emerald-200 text-emerald-900'
                  : isRunning
                  ? 'bg-blue-50/80 border-blue-300 text-blue-900'
                  : 'bg-slate-50/80 border-slate-200 text-slate-500'
              }`}
            >
              <div className="flex items-center justify-between mb-1.5">
                <span className="text-[10px] font-mono uppercase tracking-wider text-slate-500 font-medium">
                  Step 0{idx + 1}
                </span>
                {isCompleted ? (
                  <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                ) : isRunning ? (
                  <Loader2 className="w-4 h-4 text-blue-600 animate-spin" />
                ) : (
                  <Circle className="w-4 h-4 text-slate-300" />
                )}
              </div>

              <div className="font-semibold text-xs text-slate-900 truncate mb-1">
                {step.name}
              </div>

              <div className="text-[11px] text-slate-600 line-clamp-2 leading-tight">
                {step.description}
              </div>

              {step.durationMs !== undefined && isCompleted && (
                <div className="mt-2 text-[10px] font-mono text-slate-600 bg-slate-100 border border-slate-200 px-1.5 py-0.5 rounded inline-block">
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
