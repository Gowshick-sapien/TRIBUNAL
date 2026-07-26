import React from 'react';
import {
  FileText,
  Activity,
  DollarSign,
  UserCheck,
  Layers,
  Shield,
  Gavel,
  CheckCircle,
  Clock,
} from 'lucide-react';

interface ReportSidebarProps {
  activeSection: string;
  onSelectSection: (sectionId: string) => void;
}

export const ReportSidebar: React.FC<ReportSidebarProps> = ({
  activeSection,
  onSelectSection,
}) => {
  const sections = [
    { id: 'sec-summary', label: 'Executive Summary', icon: FileText },
    { id: 'sec-timeline', label: 'Investigation Timeline', icon: Clock },
    { id: 'sec-financial', label: 'Financial Findings', icon: DollarSign },
    { id: 'sec-behaviour', label: 'Behaviour Findings', icon: UserCheck },
    { id: 'sec-evidence', label: 'Evidence Graph', icon: Layers },
    { id: 'sec-defense', label: 'Defense Review', icon: Shield },
    { id: 'sec-tribunal', label: 'Tribunal Deliberation', icon: Gavel },
    { id: 'sec-recommendations', label: 'Recommendations', icon: CheckCircle },
    { id: 'sec-audit', label: 'Audit Trail', icon: Activity },
  ];

  return (
    <div className="glass-panel p-4 rounded-2xl border border-slate-800 space-y-3 font-mono text-xs w-64 shrink-0 hidden lg:block sticky top-6">
      <div className="text-[10px] text-slate-500 uppercase font-bold tracking-wider px-2">
        Report Navigator
      </div>

      <nav className="space-y-1">
        {sections.map((sec) => {
          const Icon = sec.icon;
          const isActive = activeSection === sec.id;
          return (
            <button
              key={sec.id}
              onClick={() => onSelectSection(sec.id)}
              className={`w-full text-left flex items-center gap-2.5 px-3 py-2 rounded-xl transition font-medium ${
                isActive
                  ? 'bg-cyan-500/15 text-cyan-300 border border-cyan-500/30 font-bold'
                  : 'text-slate-400 hover:bg-slate-900 hover:text-slate-200'
              }`}
            >
              <Icon className="w-4 h-4 shrink-0" />
              <span className="truncate">{sec.label}</span>
            </button>
          );
        })}
      </nav>
    </div>
  );
};
