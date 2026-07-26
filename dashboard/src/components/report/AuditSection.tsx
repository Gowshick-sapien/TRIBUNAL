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
    <div id="sec-audit" className="surface-card p-6 rounded-lg border border-slate-200 space-y-4 scroll-mt-6 shadow-xs font-sans">
      <div className="text-blue-600 font-sans text-xs font-semibold uppercase tracking-wider border-b border-slate-200 pb-2.5 flex items-center gap-2">
        <Activity className="w-4 h-4 text-blue-600" /> Section 9: Audit Trail & Pipeline Execution Timeline
      </div>

      <div className="space-y-2 font-sans text-xs">
        {steps.map((step, idx) => (
          <div key={idx} className="flex items-start gap-3 p-3 rounded-lg bg-slate-50 border border-slate-200">
            <div className="w-5 h-5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 flex items-center justify-center text-[10px] font-semibold shrink-0 mt-0.5">
              <Check className="w-3 h-3" />
            </div>
            <div>
              <span className="font-semibold text-slate-900 block">{step.title}</span>
              <span className="text-[11px] text-slate-600 font-sans">{step.desc}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
