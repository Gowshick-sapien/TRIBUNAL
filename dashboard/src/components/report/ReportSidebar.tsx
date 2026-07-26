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
    <div className="surface-card p-4 rounded-lg border border-slate-200 space-y-3 font-sans text-xs w-60 shrink-0 hidden lg:block sticky top-6 shadow-xs">
      <div className="text-[10px] text-slate-500 uppercase font-semibold tracking-wider px-2">
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
              className={`w-full text-left flex items-center gap-2.5 px-3 py-2 rounded-md transition-colors font-medium text-xs ${
                isActive
                  ? 'bg-blue-50 text-blue-700 border border-blue-200/60 font-semibold'
                  : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900 border border-transparent'
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
