import React, { useState } from 'react';
import { Settings, Save, RotateCcw, CheckCircle2, Server } from 'lucide-react';
import { DEFAULT_API_BASE, getApiBaseUrl, setApiBaseUrl } from '../services/api';

export const SettingsPage: React.FC = () => {
  const [apiUrl, setApiUrl] = useState(getApiBaseUrl());
  const [defaultDataset, setDefaultDataset] = useState('default');
  const [savedMsg, setSavedMsg] = useState(false);

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    setApiBaseUrl(apiUrl.trim());
    setSavedMsg(true);
    setTimeout(() => setSavedMsg(false), 3000);
  };

  const handleReset = () => {
    setApiUrl(DEFAULT_API_BASE);
    setApiBaseUrl(DEFAULT_API_BASE);
    setSavedMsg(true);
    setTimeout(() => setSavedMsg(false), 3000);
  };

  return (
    <div className="p-8 max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div className="border-b border-slate-800 pb-4">
        <h1 className="text-2xl font-black text-slate-100 font-sans tracking-tight flex items-center gap-2">
          <Settings className="w-6 h-6 text-cyan-400" />
          Workstation & Connection Settings
        </h1>
        <p className="text-xs font-mono text-slate-400 mt-1">
          Configure REST API base endpoints, default datasets, and dashboard preferences.
        </p>
      </div>

      {savedMsg && (
        <div className="p-3.5 rounded-xl bg-emerald-950/80 border border-emerald-800 text-emerald-300 text-xs font-mono flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          Settings saved successfully!
        </div>
      )}

      <form onSubmit={handleSave} className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-6">
        <div className="space-y-2">
          <label className="block text-xs font-mono font-semibold text-slate-300 uppercase tracking-wider flex items-center gap-2">
            <Server className="w-4 h-4 text-cyan-400" />
            Backend REST API Base URL
          </label>
          <input
            type="text"
            value={apiUrl}
            onChange={(e) => setApiUrl(e.target.value)}
            className="w-full bg-slate-900 border border-slate-700 focus:border-cyan-500 rounded-xl py-2.5 px-4 text-sm font-mono text-slate-100"
          />
          <span className="text-[11px] font-mono text-slate-500">
            Default endpoint: <code className="text-cyan-400">{DEFAULT_API_BASE}</code>
          </span>
        </div>

        <div className="space-y-2">
          <label className="block text-xs font-mono font-semibold text-slate-300 uppercase tracking-wider">
            Default Dataset Reference
          </label>
          <select
            value={defaultDataset}
            onChange={(e) => setDefaultDataset(e.target.value)}
            className="w-full bg-slate-900 border border-slate-700 focus:border-cyan-500 rounded-xl py-2.5 px-4 text-sm font-mono text-slate-200"
          >
            <option value="default">default (LI-Small_Trans.csv)</option>
            <option value="datasets/processed/transactions.parquet">processed/transactions.parquet</option>
            <option value="tribunal/datasets/LI-Small_Trans.csv">tribunal/datasets/LI-Small_Trans.csv</option>
          </select>
        </div>

        <div className="pt-4 border-t border-slate-800 flex justify-between items-center">
          <button
            type="button"
            onClick={handleReset}
            className="px-4 py-2 rounded-xl bg-slate-900 border border-slate-700 hover:border-slate-600 text-slate-400 hover:text-slate-200 font-mono text-xs transition flex items-center gap-2"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            Reset to Defaults
          </button>

          <button
            type="submit"
            className="px-6 py-2.5 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-mono font-bold text-xs transition shadow-lg shadow-cyan-500/20 flex items-center gap-2"
          >
            <Save className="w-4 h-4" />
            Save Preferences
          </button>
        </div>
      </form>
    </div>
  );
};
