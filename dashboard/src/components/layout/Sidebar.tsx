import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  Home,
  PlusCircle,
  History,
  Activity,
  Settings,
  Sparkles,
} from 'lucide-react';

export const Sidebar: React.FC = () => {
  const navItems = [
    { to: '/', label: 'Home Overview', icon: Home, exact: true },
    { to: '/investigate', label: 'New Investigation', icon: PlusCircle, highlight: true },
    { to: '/history', label: 'Investigation History', icon: History },
    { to: '/system', label: 'System & Health', icon: Activity },
    { to: '/settings', label: 'Settings', icon: Settings },
  ];

  return (
    <aside className="w-64 border-r border-slate-800 glass-panel flex flex-col justify-between p-4 shrink-0 hidden md:flex">
      <div className="space-y-6">
        {/* Section Header */}
        <div>
          <div className="text-[10px] font-mono font-semibold text-slate-500 uppercase tracking-wider px-3 mb-3">
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
                    `flex items-center gap-3 px-3 py-2.5 rounded-lg text-xs font-mono font-medium transition-all duration-200 ${
                      isActive
                        ? 'bg-cyan-500/15 text-cyan-300 border border-cyan-500/30 shadow-lg shadow-cyan-500/10'
                        : item.highlight
                        ? 'text-cyan-400 hover:bg-slate-800/80 hover:text-cyan-300 border border-cyan-950'
                        : 'text-slate-400 hover:bg-slate-800/60 hover:text-slate-200'
                    }`
                  }
                >
                  <Icon className="w-4 h-4" />
                  <span>{item.label}</span>
                </NavLink>
              );
            })}
          </nav>
        </div>

        {/* Quick Launch Card */}
        <div className="p-3.5 rounded-xl bg-gradient-to-br from-cyan-950/40 to-slate-900 border border-cyan-800/40">
          <div className="flex items-center gap-2 text-cyan-400 text-xs font-mono font-semibold mb-1">
            <Sparkles className="w-4 h-4" />
            Agentic Engine D.3
          </div>
          <p className="text-[11px] text-slate-400 leading-relaxed mb-3">
            Exposes multi-expert reasoning, evidence graphs, and adversarial tribunal deliberation.
          </p>
          <NavLink
            to="/investigate"
            className="block text-center w-full py-1.5 px-3 rounded bg-cyan-500 text-slate-950 font-mono font-bold text-xs hover:bg-cyan-400 transition shadow-md shadow-cyan-500/20"
          >
            + Run Query
          </NavLink>
        </div>
      </div>

      {/* Footer Info */}
      <div className="border-t border-slate-800/80 pt-3 text-[11px] font-mono text-slate-500 flex flex-col gap-1 px-1">
        <div className="flex justify-between">
          <span>Platform Phase</span>
          <span className="text-slate-300 font-bold">Phase D.3</span>
        </div>
        <div className="flex justify-between">
          <span>Backend REST API</span>
          <span className="text-emerald-400 font-bold">Online</span>
        </div>
      </div>
    </aside>
  );
};
