import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  Home,
  PlusCircle,
  Database,
  ArrowLeftRight,
  Activity,
  Settings,
  Sparkles,
  FileText,
} from 'lucide-react';

export const Sidebar: React.FC = () => {
  const navItems = [
    { to: '/', label: 'Home Overview', icon: Home, exact: true },
    { to: '/investigate', label: 'New Investigation', icon: PlusCircle, highlight: true },
    { to: '/history', label: 'Report Workstation', icon: FileText },
    { to: '/explorer', label: 'Repository Explorer', icon: Database },
    { to: '/compare', label: 'Compare Workspace', icon: ArrowLeftRight },
    { to: '/system', label: 'System & Health', icon: Activity },
    { to: '/settings', label: 'Settings', icon: Settings },
  ];

  return (
    <aside className="w-60 border-r border-slate-200 bg-white flex flex-col justify-between p-4 shrink-0 hidden md:flex">
      <div className="space-y-6">
        {/* Section Header */}
        <div>
          <div className="text-[10px] font-sans font-semibold text-slate-400 uppercase tracking-wider px-3 mb-2">
            Navigation Console
          </div>
          <nav className="space-y-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.to}
                  to={item.to}
                  className={({ isActive }: { isActive: boolean }) =>
                    `flex items-center gap-2.5 px-3 py-2 rounded-md text-xs font-sans transition-colors ${
                      isActive
                        ? 'bg-blue-50 text-blue-700 font-semibold border border-blue-200/60'
                        : item.highlight
                        ? 'text-blue-600 font-medium hover:bg-slate-50 hover:text-blue-700 border border-slate-200/80 bg-slate-50/50'
                        : 'text-slate-600 font-medium hover:bg-slate-50 hover:text-slate-900 border border-transparent'
                    }`
                  }
                >
                  <Icon className="w-4 h-4 shrink-0" />
                  <span>{item.label}</span>
                </NavLink>
              );
            })}
          </nav>
        </div>

        {/* Quick Launch Card */}
        <div className="p-3.5 rounded-lg bg-slate-50 border border-slate-200 space-y-2">
          <div className="flex items-center gap-1.5 text-slate-900 text-xs font-sans font-semibold">
            <Sparkles className="w-3.5 h-3.5 text-blue-600" />
            Agentic Engine Platform
          </div>
          <p className="text-[11px] text-slate-500 leading-relaxed font-sans">
            Exposes multi-expert reasoning, evidence graphs, repository search, and tribunal consensus.
          </p>
          <NavLink
            to="/investigate"
            className="block text-center w-full py-1.5 px-3 rounded-md bg-blue-600 text-white font-sans font-medium text-xs hover:bg-blue-700 transition-colors shadow-xs"
          >
            + Run Query
          </NavLink>
        </div>
      </div>

      {/* Footer Info */}
      <div className="border-t border-slate-200 pt-3 text-[11px] font-sans text-slate-500 flex flex-col gap-1 px-1">
        <div className="flex justify-between">
          <span>Platform Phase</span>
          <span className="text-slate-700 font-medium">Phase D.5</span>
        </div>
        <div className="flex justify-between">
          <span>Backend REST API</span>
          <span className="text-emerald-700 font-semibold">Online</span>
        </div>
      </div>
    </aside>
  );
};
