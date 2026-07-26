import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import {
  Play,
  Database,
  Search,
  Sparkles,
  AlertCircle,
  FileText,
  CheckCircle,
} from 'lucide-react';
import { api } from '../services/api';
import type { DatasetItemSchema, InvestigationResponse } from '../types';
import { VerdictBadge } from '../components/common/VerdictBadge';
import { RiskChip } from '../components/common/RiskChip';
import { ConfidenceMeter } from '../components/common/ConfidenceMeter';
import { ExecutionTimeline, type TimelineStep } from '../components/common/ExecutionTimeline';

export const WorkspacePage: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const [query, setQuery] = useState('');
  const [dataset, setDataset] = useState('default');
  const [availableDatasets, setAvailableDatasets] = useState<DatasetItemSchema[]>([
    { id: 'default', name: 'IBM AML Small (Default)', description: 'Default dataset', default: true },
    { id: 'li_small', name: 'IBM AML Small CSV', description: 'CSV dataset', default: false },
    { id: 'ibm_small', name: 'IBM Transactions Parquet', description: 'Parquet dataset', default: false },
    { id: 'synthetic', name: 'Synthetic AML Demo', description: 'Demo dataset', default: false },
  ]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<InvestigationResponse | null>(null);

  // Execution pipeline state
  const [steps, setSteps] = useState<TimelineStep[]>([
    { id: '1', name: 'Planner Framework', description: 'Intent parsing & execution planning', status: 'pending' },
    { id: '2', name: 'Financial Expert', description: 'Structuring & velocity pattern detection', status: 'pending' },
    { id: '3', name: 'Behaviour Expert', description: 'Baseline drift & dormancy detection', status: 'pending' },
    { id: '4', name: 'Evidence Graph', description: 'Topology synthesis & node linking', status: 'pending' },
    { id: '5', name: 'Adversarial Defense', description: 'Contradiction review & legitimate counter-hypotheses', status: 'pending' },
    { id: '6', name: 'Tribunal Consensus', description: 'Multi-hypothesis deliberation & confidence calibration', status: 'pending' },
  ]);

  useEffect(() => {
    if (location.state && location.state.initialQuery) {
      setQuery(location.state.initialQuery);
    }

    // Dynamically load datasets from GET /api/v1/datasets
    const fetchDatasets = async () => {
      try {
        const res = await api.getDatasets();
        if (res.datasets && res.datasets.length > 0) {
          setAvailableDatasets(res.datasets);
        }
      } catch (err) {
        console.warn('Could not fetch datasets dynamically from API, using fallback list:', err);
      }
    };
    fetchDatasets();
  }, [location.state]);

  const handleRunInvestigation = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!query || query.trim().length < 3) {
      setError('Please enter an investigation query (at least 3 characters).');
      return;
    }

    setError(null);
    setLoading(true);
    setResult(null);

    // Reset timeline animation steps
    setSteps((prev) => prev.map((s) => ({ ...s, status: 'pending', durationMs: undefined })));

    // Step 1: Running Planner
    setSteps((prev) => prev.map((s) => (s.id === '1' ? { ...s, status: 'running' } : s)));

    try {
      setTimeout(() => {
        setSteps((prev) =>
          prev.map((s) =>
            s.id === '1'
              ? { ...s, status: 'completed', durationMs: 12.4 }
              : s.id === '2'
              ? { ...s, status: 'running' }
              : s
          )
        );
      }, 400);

      setTimeout(() => {
        setSteps((prev) =>
          prev.map((s) =>
            s.id === '2'
              ? { ...s, status: 'completed', durationMs: 15.2 }
              : s.id === '3'
              ? { ...s, status: 'running' }
              : s
          )
        );
      }, 800);

      setTimeout(() => {
        setSteps((prev) =>
          prev.map((s) =>
            s.id === '3'
              ? { ...s, status: 'completed', durationMs: 18.6 }
              : s.id === '4'
              ? { ...s, status: 'running' }
              : s
          )
        );
      }, 1200);

      setTimeout(() => {
        setSteps((prev) =>
          prev.map((s) =>
            s.id === '4'
              ? { ...s, status: 'completed', durationMs: 8.4 }
              : s.id === '5'
              ? { ...s, status: 'running' }
              : s
          )
        );
      }, 1500);

      setTimeout(() => {
        setSteps((prev) =>
          prev.map((s) =>
            s.id === '5'
              ? { ...s, status: 'completed', durationMs: 14.1 }
              : s.id === '6'
              ? { ...s, status: 'running' }
              : s
          )
        );
      }, 1800);

      // Execute actual REST API payload to backend sending Dataset Alias ID
      const res = await api.runInvestigation({
        query,
        dataset,
        options: {
          confidence_threshold: 0.5,
          max_depth: 3,
          include_graph: true,
        },
      });

      setSteps((prev) =>
        prev.map((s) => ({
          ...s,
          status: 'completed',
          durationMs: s.durationMs || 10.0,
        }))
      );

      setResult(res);
    } catch (err: any) {
      setError(err.response?.data?.message || err.message || 'Investigation execution failed.');
      setSteps((prev) => prev.map((s) => (s.status === 'running' ? { ...s, status: 'failed' } : s)));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8">
      {/* Page Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-2xl font-black text-slate-100 font-sans tracking-tight flex items-center gap-2">
            <Sparkles className="w-6 h-6 text-cyan-400" />
            Investigation Execution Workspace
          </h1>
          <p className="text-xs font-mono text-slate-400 mt-1">
            Submit natural language queries to trigger the Phase C agentic pipeline and persist artifacts in D.2 storage.
          </p>
        </div>
      </div>

      {/* Query & Input Form */}
      <form onSubmit={handleRunInvestigation} className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1 space-y-2">
            <label className="block text-xs font-mono font-semibold text-slate-300 uppercase tracking-wider">
              Natural Language Query / Target Objective
            </label>
            <div className="relative">
              <Search className="w-5 h-5 text-slate-500 absolute left-3.5 top-3 pointer-events-none" />
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="e.g. Is customer ACC_8000A94C0 engaged in structuring and velocity anomalies?"
                className="w-full bg-slate-900/90 border border-slate-700 focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 rounded-xl py-2.5 pl-11 pr-4 text-sm font-sans text-slate-100 placeholder-slate-500 transition"
              />
            </div>
          </div>

          <div className="w-full md:w-72 space-y-2">
            <label className="block text-xs font-mono font-semibold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
              <Database className="w-3.5 h-3.5 text-cyan-400" />
              Dataset Alias ID
            </label>
            <select
              value={dataset}
              onChange={(e) => setDataset(e.target.value)}
              className="w-full bg-slate-900/90 border border-slate-700 focus:border-cyan-500 rounded-xl py-2.5 px-3 text-sm font-mono text-slate-200 transition"
            >
              {availableDatasets.map((d) => (
                <option key={d.id} value={d.id}>
                  {d.name} ({d.id})
                </option>
              ))}
            </select>
          </div>
        </div>

        {error && (
          <div className="p-3 rounded-lg bg-rose-950/60 border border-rose-800 text-rose-300 text-xs font-mono flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-rose-400 shrink-0" />
            {error}
          </div>
        )}

        <div className="flex justify-end pt-2">
          <button
            type="submit"
            disabled={loading}
            className="px-6 py-3 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 font-mono font-bold text-sm transition shadow-lg shadow-cyan-500/25 flex items-center gap-2 disabled:opacity-50"
          >
            {loading ? (
              <>
                <span className="w-4 h-4 border-2 border-slate-950 border-t-transparent rounded-full animate-spin" />
                Executing Pipeline...
              </>
            ) : (
              <>
                <Play className="w-4 h-4 fill-slate-950" />
                Run Investigation Engine
              </>
            )}
          </button>
        </div>
      </form>

      {/* Execution Timeline */}
      <ExecutionTimeline steps={steps} totalMs={result?.metrics?.total_ms} />

      {/* Result Display Card */}
      {result && (
        <div className="glass-panel p-6 rounded-2xl border border-cyan-500/30 space-y-6 animate-fadeIn">
          {/* Header */}
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-4">
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <span className="text-xs font-mono text-slate-400">ID:</span>
                <span className="font-mono text-sm font-bold text-cyan-400">{result.investigation_id}</span>
                <span className="text-[10px] font-mono bg-emerald-950 border border-emerald-800 text-emerald-300 px-2 py-0.5 rounded flex items-center gap-1">
                  <CheckCircle className="w-3 h-3" /> Persisted to Storage (D.2)
                </span>
              </div>
              <h2 className="text-lg font-bold text-slate-100 font-sans">
                {result.winning_hypothesis || 'Investigation Completed'}
              </h2>
            </div>

            <div className="flex items-center gap-3">
              <VerdictBadge verdict={result.verdict} size="lg" />
              <RiskChip risk={result.risk_level} />
            </div>
          </div>

          {/* Metrics & Confidence */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="md:col-span-2 space-y-3">
              <div className="text-xs font-mono font-semibold text-slate-400 uppercase tracking-wider">
                Executive Findings Summary
              </div>
              <p className="text-sm text-slate-200 leading-relaxed font-sans bg-slate-900/60 p-4 rounded-xl border border-slate-800">
                {result.summary}
              </p>
              <p className="text-xs text-slate-300 font-mono bg-slate-900/60 p-3 rounded-lg border border-slate-800">
                <strong>Actionable Recommendation:</strong> {result.recommendation}
              </p>
            </div>

            <div className="glass-card p-4 rounded-xl border border-slate-800 space-y-4 flex flex-col justify-between">
              <ConfidenceMeter confidence={result.confidence} />

              <div className="space-y-2 text-xs font-mono border-t border-slate-800 pt-3">
                <div className="flex justify-between">
                  <span className="text-slate-400">Planner Latency</span>
                  <span className="text-cyan-400">{result.metrics?.planner_ms?.toFixed(1) || '0.0'} ms</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Total Duration</span>
                  <span className="text-cyan-400 font-bold">{result.metrics?.total_ms?.toFixed(1) || '0.0'} ms</span>
                </div>
              </div>
            </div>
          </div>

          {/* Action Links */}
          <div className="pt-4 border-t border-slate-800 flex flex-wrap gap-3">
            <button
              onClick={() => navigate(`/investigation/${result.investigation_id}`)}
              className="px-4 py-2 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-mono font-bold text-xs transition flex items-center gap-2"
            >
              <FileText className="w-4 h-4" />
              Open Full Investigation Viewer &rarr;
            </button>
            <button
              onClick={() => navigate(`/investigation/${result.investigation_id}?tab=report`)}
              className="px-4 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-700 font-mono text-xs transition"
            >
              View 10-Section Report
            </button>
            <button
              onClick={() => navigate(`/investigation/${result.investigation_id}?tab=verdict`)}
              className="px-4 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-700 font-mono text-xs transition"
            >
              View Deliberation Trace
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
