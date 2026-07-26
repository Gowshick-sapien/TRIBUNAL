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
    <header className="h-14 border-b border-slate-200 bg-white sticky top-0 z-50 px-6 flex items-center justify-between shadow-xs">
      {/* Brand & Platform Title */}
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 rounded-lg bg-blue-600 text-white flex items-center justify-center shadow-xs">
          <Shield className="w-4 h-4 stroke-[2.2]" />
        </div>
        <div>
          <div className="flex items-center gap-2">
            <span className="font-sans font-bold text-base tracking-tight text-slate-900">
              TRIBUNAL
            </span>
            <span className="px-2 py-0.5 text-[10px] font-mono font-medium bg-slate-100 border border-slate-200 text-slate-600 rounded">
              v1.0.0
            </span>
          </div>
          <p className="text-xs text-slate-500 font-sans tracking-tight flex items-center gap-1">
            <Terminal className="w-3 h-3 text-slate-400" />
            AML Investigation Workstation Platform
          </p>
        </div>
      </div>

      {/* Center Indicator */}
      <div className="hidden md:flex items-center gap-6 text-xs">
        <div className="flex items-center gap-2 px-3 py-1 rounded-md bg-slate-50 border border-slate-200">
          <Activity className="w-3.5 h-3.5 text-blue-600" />
          <span className="text-slate-500 font-medium uppercase tracking-wider text-[10px]">Engine Status:</span>
          <span className={health?.status === 'healthy' ? 'text-emerald-700 font-semibold' : 'text-amber-700 font-semibold'}>
            {health?.status ? health.status.toUpperCase() : 'CONNECTING...'}
          </span>
        </div>
      </div>

      {/* Actions */}
      <div className="flex items-center gap-2">
        <Link
          to="/settings"
          className="p-1.5 rounded-md bg-white border border-slate-200 text-slate-600 hover:text-slate-900 hover:bg-slate-50 transition-colors"
          title="Platform Settings"
        >
          <SettingsIcon className="w-4 h-4" />
        </Link>
      </div>
    </header>
  );
};
