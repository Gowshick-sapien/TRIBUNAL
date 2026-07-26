import React, { useEffect, useState } from 'react';
import { Shield, Activity, Settings as SettingsIcon, Terminal, FileText, Search } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';
import { api } from '../../services/api';
import type { HealthResponse } from '../../types';

export const Navbar: React.FC = () => {
  const navigate = useNavigate();
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [reportSearchId, setReportSearchId] = useState('');

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

  const handleOpenReport = (e: React.FormEvent) => {
    e.preventDefault();
    if (!reportSearchId.trim()) return;
    const cleanId = reportSearchId.trim();
    const targetId = cleanId.startsWith('inv_') ? cleanId : `inv_${cleanId}`;
    navigate(`/report/${targetId}`);
    setReportSearchId('');
  };

  return (
    <header className="h-14 border-b border-slate-200 bg-white sticky top-0 z-50 px-6 flex items-center justify-between shadow-xs">
      {/* Brand & Platform Title */}
      <div className="flex items-center gap-3">
        <Link to="/" className="w-8 h-8 rounded-lg bg-blue-600 text-white flex items-center justify-center shadow-xs hover:bg-blue-700 transition-colors">
          <Shield className="w-4 h-4 stroke-[2.2]" />
        </Link>
        <div>
          <div className="flex items-center gap-2">
            <Link to="/" className="font-sans font-bold text-base tracking-tight text-slate-900 hover:text-blue-600 transition-colors">
              TRIBUNAL
            </Link>
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

      {/* Center Quick Report Search */}
      <div className="hidden lg:flex items-center gap-4 text-xs font-sans">
        <form onSubmit={handleOpenReport} className="relative flex items-center">
          <Search className="w-3.5 h-3.5 text-slate-400 absolute left-2.5 pointer-events-none" />
          <input
            type="text"
            placeholder="Open Report by ID (e.g. inv_fe096149e9c3)"
            value={reportSearchId}
            onChange={(e) => setReportSearchId(e.target.value)}
            className="pl-8 pr-16 py-1 bg-slate-50 border border-slate-200 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:bg-white rounded-md text-xs font-mono text-slate-900 placeholder-slate-400 w-72 transition-colors"
          />
          <button
            type="submit"
            className="absolute right-1 px-2 py-0.5 rounded bg-blue-600 text-white text-[10px] font-medium hover:bg-blue-700 transition-colors"
          >
            Go
          </button>
        </form>

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
          to="/history"
          className="px-2.5 py-1.5 rounded-md bg-slate-50 border border-slate-200 text-slate-700 hover:bg-slate-100 transition-colors text-xs font-medium flex items-center gap-1.5"
          title="All Reports & History"
        >
          <FileText className="w-3.5 h-3.5 text-blue-600" />
          Reports
        </Link>
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
