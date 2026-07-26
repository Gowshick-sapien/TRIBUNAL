import React, { useEffect, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import {
  ShieldAlert,
  ArrowRight,
  Zap,
  Activity,
  Layers,
  Database,
  Search,
  CheckCircle2,
} from 'lucide-react';
import { api } from '../services/api';
import type { HealthResponse, InvestigationRecordSchema, MetadataResponse } from '../types';
import { VerdictBadge } from '../components/common/VerdictBadge';
import { RiskChip } from '../components/common/RiskChip';

export const HomePage: React.FC = () => {
  const navigate = useNavigate();
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [metadata, setMetadata] = useState<MetadataResponse | null>(null);
  const [recentInv, setRecentInv] = useState<InvestigationRecordSchema[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      try {
        const [h, m, list] = await Promise.all([
          api.getHealth().catch(() => null),
          api.getMetadata().catch(() => null),
          api.listInvestigations(5).catch(() => ({ investigations: [] })),
        ]);
        setHealth(h);
        setMetadata(m);
        setRecentInv(list.investigations || []);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  const sampleQueries = [
    {
      title: 'Structuring & Velocity Analysis',
      query: 'Is customer ACC_8000A94C0 engaged in structuring and velocity anomalies?',
      target: 'ACC_8000A94C0',
      badge: 'High Signal',
    },
    {
      title: 'Dormancy & Baseline Drift',
      query: 'Check account ACC_9999B11C1 for dormancy reactivation and currency change drift',
      target: 'ACC_9999B11C1',
      badge: 'Behavioral Drift',
    },
    {
      title: 'Rapid Wire Transfer Burst',
      query: 'Investigate account ACC_7777C22D2 for high-frequency micro-transfers and counterparty behavior',
      target: 'ACC_7777C22D2',
      badge: 'Frequency Pattern',
    },
  ];

  const handleLaunchSample = (queryText: string) => {
    navigate('/investigate', { state: { initialQuery: queryText } });
  };

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8">
      {/* Banner / Hero */}
      <div className="glass-panel p-8 rounded-2xl border border-slate-800 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl -z-10 pointer-events-none" />

        <div className="max-w-3xl space-y-4">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-950/80 border border-cyan-800/50 text-cyan-300 text-xs font-mono">
            <Zap className="w-3.5 h-3.5" />
            Hackathon MVP Demonstration Station
          </div>

          <h1 className="text-3xl md:text-4xl font-black text-slate-100 tracking-tight font-sans">
            Autonomous AML Investigation & Consensus Platform
          </h1>

          <p className="text-slate-400 text-sm leading-relaxed font-sans">
            TRIBUNAL turns complex financial datasets into explainable, audit-ready investigations.
            It orchestrates natural language planning, domain investigator experts, synthesis evidence graphs,
            adversarial defense counter-explanations, and a multi-hypothesis tribunal consensus engine.
          </p>

          <div className="pt-2 flex flex-wrap gap-4">
            <button
              onClick={() => navigate('/investigate')}
              className="px-5 py-2.5 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-mono font-bold text-sm transition shadow-lg shadow-cyan-500/25 flex items-center gap-2"
            >
              <Search className="w-4 h-4" />
              Launch Investigation Workspace
              <ArrowRight className="w-4 h-4" />
            </button>
            <Link
              to="/history"
              className="px-5 py-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-700 font-mono text-sm transition flex items-center gap-2"
            >
              <Database className="w-4 h-4 text-cyan-400" />
              Browse Persistent History
            </Link>
          </div>
        </div>
      </div>

      {/* Quick Start Sample Scenarios */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-base font-mono font-bold text-slate-200 uppercase tracking-wider flex items-center gap-2">
            <Layers className="w-4 h-4 text-cyan-400" />
            Pre-Configured Demo Scenarios
          </h2>
          <span className="text-xs text-slate-400 font-mono">Click any scenario to run immediately</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {sampleQueries.map((item, i) => (
            <div
              key={i}
              onClick={() => handleLaunchSample(item.query)}
              className="glass-card p-5 rounded-xl border border-slate-800 hover:border-cyan-500/50 hover:bg-slate-800/80 transition cursor-pointer group flex flex-col justify-between"
            >
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-cyan-950 text-cyan-300 border border-cyan-800">
                    {item.badge}
                  </span>
                  <ArrowRight className="w-4 h-4 text-slate-600 group-hover:text-cyan-400 transition" />
                </div>
                <h3 className="font-bold text-sm text-slate-100 group-hover:text-cyan-300 transition">
                  {item.title}
                </h3>
                <p className="text-xs text-slate-400 font-mono line-clamp-2">
                  "{item.query}"
                </p>
              </div>

              <div className="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-500 font-mono">
                <span>Target: {item.target}</span>
                <span className="text-cyan-400 group-hover:underline">Run Scenario &rarr;</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Grid: Platform Health Status & Supported AML Patterns */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Platform Status */}
        <div className="glass-card p-5 rounded-xl border border-slate-800 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <h3 className="font-mono text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-2">
              <Activity className="w-4 h-4 text-cyan-400" />
              Engine Status
            </h3>
            <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-emerald-950 text-emerald-400 border border-emerald-800">
              {health?.status || 'ONLINE'}
            </span>
          </div>

          <div className="space-y-2.5 text-xs font-mono">
            <div className="flex justify-between items-center">
              <span className="text-slate-400">REST API Version</span>
              <span className="text-slate-200 font-bold">{health?.api_version || 'v1'}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-slate-400">Planner Module</span>
              <span className="text-emerald-400 flex items-center gap-1 font-bold">
                <CheckCircle2 className="w-3.5 h-3.5" /> Ready
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-slate-400">Tribunal Consensus</span>
              <span className="text-emerald-400 flex items-center gap-1 font-bold">
                <CheckCircle2 className="w-3.5 h-3.5" /> Ready
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-slate-400">Uptime</span>
              <span className="text-cyan-400 font-bold">
                {health?.uptime_seconds ? `${health.uptime_seconds.toFixed(0)}s` : 'Active'}
              </span>
            </div>
          </div>
        </div>

        {/* Supported AML Patterns */}
        <div className="md:col-span-2 glass-card p-5 rounded-xl border border-slate-800 space-y-4">
          <div className="border-b border-slate-800 pb-3">
            <h3 className="font-mono text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-2">
              <ShieldAlert className="w-4 h-4 text-cyan-400" />
              Supported Domain Expert AML Detectors
            </h3>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-5 gap-2">
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
                className="px-2.5 py-1.5 rounded bg-slate-900/80 border border-slate-800 text-[11px] font-mono text-slate-300 text-center capitalize"
              >
                {pat.replace('_', ' ')}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Recent Persistent Investigations Feed */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-base font-mono font-bold text-slate-200 uppercase tracking-wider">
            Recent Persistent Investigations
          </h2>
          <Link to="/history" className="text-xs font-mono text-cyan-400 hover:underline">
            View All History &rarr;
          </Link>
        </div>

        {loading ? (
          <div className="p-8 text-center text-slate-500 font-mono text-xs">Loading persistent records...</div>
        ) : recentInv.length === 0 ? (
          <div className="glass-card p-6 rounded-xl border border-slate-800 text-center space-y-2">
            <p className="text-slate-400 text-sm">No investigations persisted yet.</p>
            <button
              onClick={() => navigate('/investigate')}
              className="text-xs font-mono text-cyan-400 hover:underline"
            >
              Run your first investigation now &rarr;
            </button>
          </div>
        ) : (
          <div className="glass-card rounded-xl border border-slate-800 overflow-hidden">
            <div className="divide-y divide-slate-800/80">
              {recentInv.map((inv) => (
                <div
                  key={inv.id}
                  onClick={() => navigate(`/investigation/${inv.id}`)}
                  className="p-4 hover:bg-slate-800/50 transition cursor-pointer flex flex-col md:flex-row md:items-center justify-between gap-4"
                >
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-xs font-bold text-cyan-400">{inv.id}</span>
                      <VerdictBadge verdict={inv.risk_level === 'HIGH' || inv.risk_level === 'CRITICAL' ? 'LIKELY_MALICIOUS' : 'INCONCLUSIVE'} size="sm" />
                      <RiskChip risk={inv.risk_level} />
                    </div>
                    <p className="text-xs text-slate-200 font-medium line-clamp-1">{inv.query}</p>
                  </div>

                  <div className="flex items-center gap-6 text-xs font-mono text-slate-400 shrink-0">
                    <div>Confidence: {(inv.confidence * 100).toFixed(0)}%</div>
                    <div>{inv.created_at ? new Date(inv.created_at).toLocaleTimeString() : 'Recent'}</div>
                    <ArrowRight className="w-4 h-4 text-slate-500" />
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
