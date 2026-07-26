import React from 'react';
import { Activity, Check } from 'lucide-react';

export const AuditSection: React.FC = () => {
  const steps = [
    { title: 'Execution Planning', desc: 'Parsed target intent & initialized candidate selector' },
    { title: 'Financial & Behaviour Inspection', desc: 'Generated 121 raw cards evaluating velocity & structuring' },
    { title: 'Evidence Graph Construction', desc: 'Inferred semantic edges and built DAG topology' },
    { title: 'Adversarial Defense Counter-Review', desc: 'Tested 2 alternative legitimate hypotheses' },
    { title: 'Tribunal Deliberation', desc: 'Calculated consensus verdict & calibrated risk' },
    { title: 'Report Generation', desc: 'Persisted immutable report artifact to D.2 repository' },
  ];

  return (
    <div id="sec-audit" className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4 scroll-mt-6">
      <div className="text-cyan-400 font-mono text-xs font-bold uppercase tracking-wider border-b border-slate-800 pb-2 flex items-center gap-2">
        <Activity className="w-4 h-4" /> Section 9: Audit Trail & Pipeline Execution Timeline
      </div>

      <div className="space-y-3 font-mono text-xs">
        {steps.map((step, idx) => (
          <div key={idx} className="flex items-start gap-3 p-3 rounded-xl bg-slate-900/60 border border-slate-800">
            <div className="w-5 h-5 rounded-full bg-cyan-950 text-cyan-400 border border-cyan-800 flex items-center justify-center text-[10px] font-bold shrink-0 mt-0.5">
              <Check className="w-3 h-3" />
            </div>
            <div>
              <span className="font-bold text-slate-200 block">{step.title}</span>
              <span className="text-[11px] text-slate-400 font-sans">{step.desc}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
