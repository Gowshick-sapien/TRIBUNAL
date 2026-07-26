import React, { useEffect, useState } from 'react';
import { Shield, Activity, Settings as SettingsIcon, Terminal } from 'lucide-react';
import { Link } from 'react-router-dom';
import { api } from '../../services/api';
import type { HealthResponse } from '../../types';

export const Navbar: React.FC = () => {
  const [health, setHealth] = useState<HealthResponse | null>(null);

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const data = await api.getHealth();
        setHealth(data);
      } catch {
        setHealth(null);
      }
    };
    checkHealth();
    const interval = setInterval(checkHealth, 15000);
    return () => clearInterval(interval);
  }, []);

  return (
    <header className="h-16 border-b border-slate-800 glass-panel sticky top-0 z-50 px-6 flex items-center justify-between">
      {/* Brand & Terminal Designation */}
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-500 to-blue-600 p-0.5 shadow-lg shadow-cyan-500/20 flex items-center justify-center">
          <Shield className="w-6 h-6 text-slate-950 stroke-[2.5]" />
        </div>
        <div>
          <div className="flex items-center gap-2">
            <span className="font-mono font-black text-lg tracking-wider text-slate-100">
              TRIBUNAL
            </span>
            <span className="px-2 py-0.5 text-[10px] font-mono font-semibold bg-cyan-950 border border-cyan-800 text-cyan-300 rounded">
              v1.0.0
            </span>
          </div>
          <p className="text-[11px] text-slate-400 font-mono tracking-tight flex items-center gap-1">
            <Terminal className="w-3 h-3 text-cyan-400" />
            AML Investigation Workstation Platform
          </p>
        </div>
      </div>

      {/* Center Indicator */}
      <div className="hidden md:flex items-center gap-6 text-xs font-mono">
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-900/80 border border-slate-800">
          <Activity className="w-3.5 h-3.5 text-cyan-400 animate-pulse" />
          <span className="text-slate-400">ENGINE STATUS:</span>
          <span className={health?.status === 'healthy' ? 'text-emerald-400 font-bold' : 'text-amber-400 font-bold'}>
            {health?.status ? health.status.toUpperCase() : 'CONNECTING...'}
          </span>
        </div>
      </div>

      {/* Actions */}
      <div className="flex items-center gap-3">
        <Link
          to="/settings"
          className="p-2 rounded-lg bg-slate-900 border border-slate-800 text-slate-400 hover:text-cyan-400 hover:border-cyan-800/50 transition"
          title="Platform Settings"
        >
          <SettingsIcon className="w-4 h-4" />
        </Link>
      </div>
    </header>
  );
};
