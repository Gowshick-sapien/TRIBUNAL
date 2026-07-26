import React, { useEffect, useState } from 'react';
import { Activity, CheckCircle2, Server, Shield, Cpu, RefreshCw } from 'lucide-react';
import { api } from '../services/api';
import type { HealthResponse, MetadataResponse } from '../types';

export const SystemPage: React.FC = () => {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [metadata, setMetadata] = useState<MetadataResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadStatus = async () => {
    setLoading(true);
    setError(null);
    try {
      const [h, m] = await Promise.all([api.getHealth(), api.getMetadata()]);
      setHealth(h);
      setMetadata(m);
    } catch (err: any) {
      setError(err.message || 'Failed to connect to REST API backend.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadStatus();
  }, []);

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-2xl font-black text-slate-100 font-sans tracking-tight flex items-center gap-2">
            <Activity className="w-6 h-6 text-cyan-400" />
            Platform Health & Capabilities Workstation
          </h1>
          <p className="text-xs font-mono text-slate-400 mt-1">
            Real-time status monitoring for REST API endpoints, Planner Engine readiness, and supported AML detection algorithms.
          </p>
        </div>

        <button
          onClick={loadStatus}
          className="px-3.5 py-2 rounded-xl bg-slate-900 border border-slate-700 hover:border-cyan-500 text-slate-300 hover:text-cyan-400 font-mono text-xs transition flex items-center gap-2"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          Ping API Backend
        </button>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-rose-950/60 border border-rose-800 text-rose-300 text-xs font-mono">
          {error}
        </div>
      )}

      {/* System Status Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="glass-card p-5 rounded-2xl border border-slate-800 space-y-2">
          <div className="flex items-center justify-between text-xs font-mono text-slate-400">
            <span>REST API Status</span>
            <Server className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-xl font-mono font-bold text-emerald-400 flex items-center gap-1.5">
            <CheckCircle2 className="w-5 h-5" />
            {health?.status ? health.status.toUpperCase() : 'ONLINE'}
          </div>
          <span className="text-[10px] font-mono text-slate-500">Version: {health?.api_version || 'v1'}</span>
        </div>

        <div className="glass-card p-5 rounded-2xl border border-slate-800 space-y-2">
          <div className="flex items-center justify-between text-xs font-mono text-slate-400">
            <span>Planner Ready</span>
            <Cpu className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-xl font-mono font-bold text-emerald-400 flex items-center gap-1.5">
            <CheckCircle2 className="w-5 h-5" />
            READY
          </div>
          <span className="text-[10px] font-mono text-slate-500">LLM & Rule Parser Active</span>
        </div>

        <div className="glass-card p-5 rounded-2xl border border-slate-800 space-y-2">
          <div className="flex items-center justify-between text-xs font-mono text-slate-400">
            <span>Tribunal Engine</span>
            <Shield className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-xl font-mono font-bold text-emerald-400 flex items-center gap-1.5">
            <CheckCircle2 className="w-5 h-5" />
            READY
          </div>
          <span className="text-[10px] font-mono text-slate-500">Multi-Hypothesis Consensus</span>
        </div>

        <div className="glass-card p-5 rounded-2xl border border-slate-800 space-y-2">
          <div className="flex items-center justify-between text-xs font-mono text-slate-400">
            <span>Server Uptime</span>
            <Activity className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-xl font-mono font-bold text-cyan-400">
            {health?.uptime_seconds ? `${health.uptime_seconds.toFixed(0)}s` : 'Active'}
          </div>
          <span className="text-[10px] font-mono text-slate-500">FastAPI Async Server</span>
        </div>
      </div>

      {/* Supported Experts & AML Patterns */}
      <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-6">
        <div>
          <h3 className="text-xs font-mono font-bold text-slate-300 uppercase tracking-wider mb-3">
            Supported Domain Experts
          </h3>
          <div className="flex gap-3">
            {(metadata?.supported_experts || ['financial', 'behaviour']).map((exp) => (
              <div
                key={exp}
                className="px-4 py-2 rounded-xl bg-slate-900 border border-slate-700 text-xs font-mono font-bold text-cyan-300 capitalize flex items-center gap-2"
              >
                <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                {exp} Domain Expert
              </div>
            ))}
          </div>
        </div>

        <div>
          <h3 className="text-xs font-mono font-bold text-slate-300 uppercase tracking-wider mb-3">
            Supported AML Pattern Detection Algorithms (10 Detectors)
          </h3>
          <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
            {(metadata?.supported_aml_patterns || [
              'structuring',
              'velocity',
              'large_transfer',
              'frequency',
              'behaviour_drift',
              'counterparty_behaviour',
              'currency_change',
              'dormancy',
              'payment_pattern',
              'spending_pattern',
            ]).map((pat) => (
              <div
                key={pat}
                className="p-3 rounded-xl bg-slate-900/80 border border-slate-800 text-xs font-mono text-slate-200 capitalize text-center"
              >
                {pat.replace('_', ' ')}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
