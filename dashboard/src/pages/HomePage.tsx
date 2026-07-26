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
    <div className="p-6 md:p-8 max-w-7xl mx-auto space-y-8 font-sans">
      {/* Banner / Hero */}
      <div className="surface-card p-8 rounded-lg border border-slate-200 relative overflow-hidden bg-white shadow-xs">
        <div className="max-w-3xl space-y-4">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-blue-50 border border-blue-200 text-blue-700 text-xs font-medium">
            <Zap className="w-3.5 h-3.5 text-blue-600" />
            Hackathon MVP Demonstration Station
          </div>

          <h1 className="text-2xl md:text-3xl font-bold text-slate-900 tracking-tight font-sans">
            Autonomous AML Investigation & Consensus Platform
          </h1>

          <p className="text-slate-600 text-sm leading-relaxed font-sans">
            TRIBUNAL turns complex financial datasets into explainable, audit-ready investigations.
            It orchestrates natural language planning, domain investigator experts, synthesis evidence graphs,
            adversarial defense counter-explanations, and a multi-hypothesis tribunal consensus engine.
          </p>

          <div className="pt-2 flex flex-wrap gap-3">
            <button
              onClick={() => navigate('/investigate')}
              className="px-4 py-2 rounded-md bg-blue-600 hover:bg-blue-700 text-white font-medium text-xs transition-colors shadow-xs flex items-center gap-2"
            >
              <Search className="w-4 h-4" />
              Launch Investigation Workspace
              <ArrowRight className="w-4 h-4" />
            </button>
            <Link
              to="/history"
              className="px-4 py-2 rounded-md bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 font-medium text-xs transition-colors shadow-xs flex items-center gap-2"
            >
              <Database className="w-4 h-4 text-blue-600" />
              Browse Persistent History
            </Link>
          </div>
        </div>
      </div>

      {/* Quick Start Sample Scenarios */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-sans font-semibold text-slate-900 uppercase tracking-wider flex items-center gap-2">
            <Layers className="w-4 h-4 text-blue-600" />
            Pre-Configured Demo Scenarios
          </h2>
          <span className="text-xs text-slate-500 font-sans">Click any scenario to run immediately</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {sampleQueries.map((item, i) => (
            <div
              key={i}
              onClick={() => handleLaunchSample(item.query)}
              className="surface-card p-5 rounded-lg border border-slate-200 hover:border-blue-300 hover:bg-slate-50/50 transition-colors cursor-pointer group flex flex-col justify-between shadow-xs"
            >
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-sans font-medium px-2 py-0.5 rounded bg-blue-50 text-blue-700 border border-blue-200">
                    {item.badge}
                  </span>
                  <ArrowRight className="w-4 h-4 text-slate-400 group-hover:text-blue-600 transition-colors" />
                </div>
                <h3 className="font-semibold text-sm text-slate-900 group-hover:text-blue-600 transition-colors">
                  {item.title}
                </h3>
                <p className="text-xs text-slate-500 font-sans line-clamp-2">
                  "{item.query}"
                </p>
              </div>

              <div className="mt-4 pt-3 border-t border-slate-200 flex items-center justify-between text-[11px] text-slate-500 font-sans">
                <span>Target: <strong className="font-mono text-slate-700">{item.target}</strong></span>
                <span className="text-blue-600 font-medium group-hover:underline">Run Scenario &rarr;</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Grid: Platform Health Status & Supported AML Patterns */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Platform Status */}
        <div className="surface-card p-5 rounded-lg border border-slate-200 space-y-4 shadow-xs">
          <div className="flex items-center justify-between border-b border-slate-200 pb-3">
            <h3 className="font-sans text-xs font-semibold text-slate-900 uppercase tracking-wider flex items-center gap-2">
              <Activity className="w-4 h-4 text-blue-600" />
              Engine Status
            </h3>
            <span className="px-2 py-0.5 rounded text-[10px] font-mono font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
              {health?.status || 'ONLINE'}
            </span>
          </div>

          <div className="space-y-2.5 text-xs font-sans">
            <div className="flex justify-between items-center">
              <span className="text-slate-500">REST API Version</span>
              <span className="text-slate-900 font-mono font-semibold">{health?.api_version || 'v1'}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-slate-500">Planner Module</span>
              <span className="text-emerald-700 flex items-center gap-1 font-semibold">
                <CheckCircle2 className="w-3.5 h-3.5" /> Ready
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-slate-500">Tribunal Consensus</span>
              <span className="text-emerald-700 flex items-center gap-1 font-semibold">
                <CheckCircle2 className="w-3.5 h-3.5" /> Ready
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-slate-500">Uptime</span>
              <span className="text-blue-600 font-mono font-semibold">
                {health?.uptime_seconds ? `${health.uptime_seconds.toFixed(0)}s` : 'Active'}
              </span>
            </div>
          </div>
        </div>

        {/* Supported AML Patterns */}
        <div className="md:col-span-2 surface-card p-5 rounded-lg border border-slate-200 space-y-4 shadow-xs">
          <div className="border-b border-slate-200 pb-3">
            <h3 className="font-sans text-xs font-semibold text-slate-900 uppercase tracking-wider flex items-center gap-2">
              <ShieldAlert className="w-4 h-4 text-blue-600" />
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
                className="px-2.5 py-1.5 rounded bg-slate-50 border border-slate-200 text-[11px] font-sans text-slate-700 text-center capitalize font-medium"
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
          <h2 className="text-sm font-sans font-semibold text-slate-900 uppercase tracking-wider">
            Recent Persistent Investigations
          </h2>
          <Link to="/history" className="text-xs font-sans text-blue-600 hover:underline font-medium">
            View All History &rarr;
          </Link>
        </div>

        {loading ? (
          <div className="p-8 text-center text-slate-500 font-sans text-xs">Loading persistent records...</div>
        ) : recentInv.length === 0 ? (
          <div className="surface-card p-6 rounded-lg border border-slate-200 text-center space-y-2">
            <p className="text-slate-600 text-sm">No investigations persisted yet.</p>
            <button
              onClick={() => navigate('/investigate')}
              className="text-xs font-sans text-blue-600 hover:underline font-medium"
            >
              Run your first investigation now &rarr;
            </button>
          </div>
        ) : (
          <div className="surface-card rounded-lg border border-slate-200 overflow-hidden shadow-xs">
            <div className="divide-y divide-slate-100">
              {recentInv.map((inv) => (
                <div
                  key={inv.id}
                  onClick={() => navigate(`/investigation/${inv.id}`)}
                  className="p-4 hover:bg-slate-50/80 transition-colors cursor-pointer flex flex-col md:flex-row md:items-center justify-between gap-4"
                >
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-xs font-semibold text-blue-600">{inv.id}</span>
                      <VerdictBadge verdict={inv.risk_level === 'HIGH' || inv.risk_level === 'CRITICAL' ? 'LIKELY_MALICIOUS' : 'INCONCLUSIVE'} size="sm" />
                      <RiskChip risk={inv.risk_level} />
                    </div>
                    <p className="text-xs text-slate-900 font-medium line-clamp-1 font-sans">{inv.query}</p>
                  </div>

                  <div className="flex items-center gap-6 text-xs font-sans text-slate-500 shrink-0">
                    <div>Confidence: <span className="font-mono font-semibold text-slate-900">{(inv.confidence * 100).toFixed(0)}%</span></div>
                    <div>{inv.created_at ? new Date(inv.created_at).toLocaleTimeString() : 'Recent'}</div>
                    <ArrowRight className="w-4 h-4 text-slate-400" />
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
