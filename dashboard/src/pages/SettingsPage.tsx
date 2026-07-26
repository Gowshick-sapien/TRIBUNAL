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
    <div className="p-6 md:p-8 max-w-4xl mx-auto space-y-6 font-sans">
      {/* Header */}
      <div className="border-b border-slate-200 pb-4">
        <h1 className="text-2xl font-bold text-slate-900 font-sans tracking-tight flex items-center gap-2">
          <Settings className="w-5 h-5 text-blue-600" />
          Workstation & Connection Settings
        </h1>
        <p className="text-xs font-sans text-slate-500 mt-1">
          Configure REST API base endpoints, default datasets, and dashboard preferences.
        </p>
      </div>

      {savedMsg && (
        <div className="p-3.5 rounded-lg bg-emerald-50 border border-emerald-200 text-emerald-700 text-xs font-sans flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 text-emerald-600" />
          Settings saved successfully!
        </div>
      )}

      <form onSubmit={handleSave} className="surface-card p-6 rounded-lg border border-slate-200 space-y-6 bg-white shadow-xs">
        <div className="space-y-2">
          <label className="block text-xs font-sans font-semibold text-slate-700 uppercase tracking-wider flex items-center gap-2">
            <Server className="w-4 h-4 text-blue-600" />
            Backend REST API Base URL
          </label>
          <input
            type="text"
            value={apiUrl}
            onChange={(e) => setApiUrl(e.target.value)}
            className="w-full bg-white border border-slate-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 rounded-md py-2 px-3 text-xs font-sans text-slate-900"
          />
          <span className="text-[11px] font-sans text-slate-500">
            Default endpoint: <code className="text-blue-600 font-mono">{DEFAULT_API_BASE}</code>
          </span>
        </div>

        <div className="space-y-2">
          <label className="block text-xs font-sans font-semibold text-slate-700 uppercase tracking-wider">
            Default Dataset Reference
          </label>
          <select
            value={defaultDataset}
            onChange={(e) => setDefaultDataset(e.target.value)}
            className="w-full bg-white border border-slate-200 focus:border-blue-500 rounded-md py-2 px-3 text-xs font-sans text-slate-900"
          >
            <option value="default">default (LI-Small_Trans.csv)</option>
            <option value="datasets/processed/transactions.parquet">processed/transactions.parquet</option>
            <option value="tribunal/datasets/LI-Small_Trans.csv">tribunal/datasets/LI-Small_Trans.csv</option>
          </select>
        </div>

        <div className="pt-4 border-t border-slate-200 flex justify-between items-center">
          <button
            type="button"
            onClick={handleReset}
            className="px-4 py-2 rounded-md bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 font-sans font-medium text-xs transition-colors flex items-center gap-2 shadow-xs"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            Reset to Defaults
          </button>

          <button
            type="submit"
            className="px-5 py-2 rounded-md bg-blue-600 hover:bg-blue-700 text-white font-medium text-xs transition-colors shadow-xs flex items-center gap-2"
          >
            <Save className="w-4 h-4" />
            Save Preferences
          </button>
        </div>
      </form>
    </div>
  );
};
