import React, { useEffect, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import {
  ArrowRight,
  Zap,
  Activity,
  Layers,
  Database,
  Search,
  CheckCircle2,
  FileText,
  ExternalLink,
} from 'lucide-react';
import { api } from '../services/api';
import type { InvestigationRecordSchema, MetadataResponse } from '../types';
import { VerdictBadge } from '../components/common/VerdictBadge';
import { RiskChip } from '../components/common/RiskChip';

export const HomePage: React.FC = () => {
  const navigate = useNavigate();
  const [metadata, setMetadata] = useState<MetadataResponse | null>(null);
  const [recentInv, setRecentInv] = useState<InvestigationRecordSchema[]>([]);
  const [loading, setLoading] = useState(true);
  const [lookupId, setLookupId] = useState('');

  useEffect(() => {
    const loadData = async () => {
      try {
        const [m, list] = await Promise.all([
          api.getMetadata().catch(() => null),
          api.listInvestigations(5).catch(() => ({ investigations: [] })),
        ]);
        setMetadata(m);
        setRecentInv(list.investigations || []);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  const handleDirectLookup = (e: React.FormEvent) => {
    e.preventDefault();
    if (!lookupId.trim()) return;
    const cleanId = lookupId.trim();
    const targetId = cleanId.startsWith('inv_') ? cleanId : `inv_${cleanId}`;
    navigate(`/report/${targetId}`);
  };

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
            TRIBUNAL Multi-Expert AI Platform
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
              <FileText className="w-4 h-4 text-blue-600" />
              Browse Report Workstation & History
            </Link>
          </div>
        </div>
      </div>

      {/* Direct Report Workstation Lookup Bar */}
      <div className="surface-card p-4 rounded-lg border border-slate-200 bg-slate-50/60 flex flex-col md:flex-row md:items-center justify-between gap-4 font-sans shadow-xs">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-lg bg-blue-100/80 text-blue-700 shrink-0">
            <FileText className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider">Direct Report Workstation Access</h3>
            <p className="text-[11px] text-slate-500">Paste any Case ID to open the interactive 10-section compliance report directly</p>
          </div>
        </div>

        <form onSubmit={handleDirectLookup} className="flex items-center gap-2 w-full md:w-auto">
          <input
            type="text"
            placeholder="e.g. inv_fe096149e9c3"
            value={lookupId}
            onChange={(e) => setLookupId(e.target.value)}
            className="px-3 py-2 bg-white border border-slate-200 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 rounded-md text-xs font-mono text-slate-900 placeholder-slate-400 w-full md:w-64 transition-colors"
          />
          <button
            type="submit"
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-md text-xs font-medium transition-colors shrink-0 shadow-xs flex items-center gap-1.5"
          >
            Open Report &rarr;
          </button>
        </form>
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
              className="surface-card p-5 rounded-lg border border-slate-200 hover:border-blue-300 hover:shadow-sm transition-all cursor-pointer space-y-3 flex flex-col justify-between bg-white"
            >
              <div className="space-y-2">
                <div className="flex justify-between items-start">
                  <span className="px-2 py-0.5 rounded bg-blue-50 text-blue-700 text-[10px] font-medium border border-blue-100 font-sans">
                    {item.badge}
                  </span>
                  <span className="text-[10px] font-mono text-slate-400 font-medium">Target: {item.target}</span>
                </div>
                <h3 className="text-sm font-semibold text-slate-900 font-sans">{item.title}</h3>
                <p className="text-xs text-slate-600 line-clamp-2 font-sans bg-slate-50 p-2.5 rounded border border-slate-100">
                  "{item.query}"
                </p>
              </div>

              <div className="pt-2 border-t border-slate-100 flex justify-between items-center text-xs text-blue-600 font-medium font-sans">
                <span>Run Investigation Engine</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Platform Capabilities & Domain Detectors */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="surface-card p-6 rounded-lg border border-slate-200 space-y-4 bg-white shadow-xs">
          <h2 className="text-sm font-sans font-semibold text-slate-900 uppercase tracking-wider flex items-center gap-2">
            <Activity className="w-4 h-4 text-blue-600" />
            Core Platform Architecture
          </h2>
          <div className="space-y-2 text-xs font-sans text-slate-600">
            <div className="flex items-start gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
              <span><strong>NL Query Planning (Qwen LLM):</strong> Converts free-form natural language into structured execution plans.</span>
            </div>
            <div className="flex items-start gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
              <span><strong>Multi-Expert Analysis:</strong> Financial & Behavioural experts generate evidence cards independently.</span>
            </div>
            <div className="flex items-start gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
              <span><strong>Adversarial Review:</strong> Defense Agent generates alternative business explanations and rebuttals.</span>
            </div>
            <div className="flex items-start gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
              <span><strong>Tribunal Consensus Engine:</strong> Weighs prosecution vs defense evidence with deterministic confidence calibration.</span>
            </div>
          </div>
        </div>

        <div className="surface-card p-6 rounded-lg border border-slate-200 space-y-4 bg-white shadow-xs">
          <h2 className="text-sm font-sans font-semibold text-slate-900 uppercase tracking-wider flex items-center gap-2">
            <Database className="w-4 h-4 text-blue-600" />
            Supported Pattern Detectors
          </h2>
          <div className="grid grid-cols-2 gap-2">
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
          <h2 className="text-sm font-sans font-semibold text-slate-900 uppercase tracking-wider flex items-center gap-2">
            <FileText className="w-4 h-4 text-blue-600" />
            Recent Persistent Investigation Reports
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
                  className="p-4 hover:bg-slate-50/80 transition-colors flex flex-col md:flex-row md:items-center justify-between gap-4"
                >
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => navigate(`/report/${inv.id}`)}
                        className="font-mono text-xs font-semibold text-blue-600 hover:underline flex items-center gap-1"
                        title="Open 10-Section Interactive Report"
                      >
                        <span>{inv.id}</span>
                        <ExternalLink className="w-3 h-3 text-blue-500" />
                      </button>
                      <VerdictBadge verdict={inv.risk_level === 'HIGH' || inv.risk_level === 'CRITICAL' ? 'LIKELY_MALICIOUS' : 'INCONCLUSIVE'} size="sm" />
                      <RiskChip risk={inv.risk_level} />
                    </div>
                    <p className="text-xs text-slate-900 font-medium line-clamp-1 font-sans">{inv.query}</p>
                  </div>

                  <div className="flex items-center gap-4 text-xs font-sans text-slate-500 shrink-0">
                    <div>Confidence: <span className="font-mono font-semibold text-slate-900">{(inv.confidence * 100).toFixed(0)}%</span></div>
                    <div>{inv.created_at ? new Date(inv.created_at).toLocaleTimeString() : 'Recent'}</div>

                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => navigate(`/report/${inv.id}`)}
                        className="px-3 py-1.5 rounded-md bg-blue-600 hover:bg-blue-700 text-white font-medium text-xs transition-colors flex items-center gap-1 shadow-xs"
                      >
                        <FileText className="w-3.5 h-3.5" />
                        Open Report
                      </button>
                      <button
                        onClick={() => navigate(`/investigation/${inv.id}`)}
                        className="px-3 py-1.5 rounded-md bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 font-medium text-xs transition-colors"
                      >
                        View Case
                      </button>
                    </div>
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
