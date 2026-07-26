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
    <div className="p-6 md:p-8 max-w-7xl mx-auto space-y-6 font-sans">
      {/* Page Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 pb-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 font-sans tracking-tight flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-blue-600" />
            Investigation Execution Workspace
          </h1>
          <p className="text-xs font-sans text-slate-500 mt-1">
            Submit natural language queries to trigger the Phase C agentic pipeline and persist artifacts in D.2 storage.
          </p>
        </div>
      </div>

      {/* Query & Input Form */}
      <form onSubmit={handleRunInvestigation} className="surface-card p-6 rounded-lg border border-slate-200 space-y-4 shadow-xs bg-white">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1 space-y-2">
            <label className="block text-xs font-sans font-semibold text-slate-700 uppercase tracking-wider">
              Natural Language Query / Target Objective
            </label>
            <div className="relative">
              <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3 pointer-events-none" />
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="e.g. Is customer ACC_8000A94C0 engaged in structuring and velocity anomalies?"
                className="w-full bg-white border border-slate-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 rounded-md py-2 pl-10 pr-4 text-xs font-sans text-slate-900 placeholder-slate-400 transition-colors"
              />
            </div>
          </div>

          <div className="w-full md:w-72 space-y-2">
            <label className="block text-xs font-sans font-semibold text-slate-700 uppercase tracking-wider flex items-center gap-1.5">
              <Database className="w-3.5 h-3.5 text-blue-600" />
              Dataset Alias ID
            </label>
            <select
              value={dataset}
              onChange={(e) => setDataset(e.target.value)}
              className="w-full bg-white border border-slate-200 focus:border-blue-500 rounded-md py-2 px-3 text-xs font-sans text-slate-900 transition-colors"
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
          <div className="p-3 rounded-md bg-rose-50 border border-rose-200 text-rose-700 text-xs font-sans flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-rose-600 shrink-0" />
            {error}
          </div>
        )}

        <div className="flex justify-end pt-2">
          <button
            type="submit"
            disabled={loading}
            className="px-5 py-2.5 rounded-md bg-blue-600 hover:bg-blue-700 text-white font-medium text-xs transition-colors shadow-xs flex items-center gap-2 disabled:opacity-50"
          >
            {loading ? (
              <>
                <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                Executing Pipeline...
              </>
            ) : (
              <>
                <Play className="w-3.5 h-3.5 fill-white" />
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
        <div className="surface-card p-6 rounded-lg border border-slate-200 space-y-6 bg-white shadow-xs">
          {/* Header */}
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 pb-4">
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <span className="text-xs font-sans text-slate-500">ID:</span>
                <span className="font-mono text-sm font-semibold text-blue-600">{result.investigation_id}</span>
                <span className="text-[10px] font-sans bg-emerald-50 border border-emerald-200 text-emerald-700 px-2 py-0.5 rounded-md flex items-center gap-1 font-medium">
                  <CheckCircle className="w-3 h-3" /> Persisted to Storage (D.2)
                </span>
              </div>
              <h2 className="text-lg font-bold text-slate-900 font-sans">
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
              <div className="text-xs font-sans font-semibold text-slate-700 uppercase tracking-wider">
                Executive Findings Summary
              </div>
              <p className="text-sm text-slate-800 leading-relaxed font-sans bg-slate-50 p-4 rounded-lg border border-slate-200">
                {result.summary}
              </p>
              <p className="text-xs text-slate-800 font-sans bg-slate-50 p-3 rounded-lg border border-slate-200">
                <strong className="text-slate-900">Actionable Recommendation:</strong> {result.recommendation}
              </p>
            </div>

            <div className="surface-card p-4 rounded-lg border border-slate-200 space-y-4 flex flex-col justify-between bg-white">
              <ConfidenceMeter confidence={result.confidence} />

              <div className="space-y-2 text-xs font-sans border-t border-slate-200 pt-3">
                <div className="flex justify-between">
                  <span className="text-slate-500">Planner Latency</span>
                  <span className="text-blue-600 font-mono font-semibold">{result.metrics?.planner_ms?.toFixed(1) || '0.0'} ms</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">Total Duration</span>
                  <span className="text-blue-600 font-mono font-semibold">{result.metrics?.total_ms?.toFixed(1) || '0.0'} ms</span>
                </div>
              </div>
            </div>
          </div>

          {/* Action Links */}
          <div className="pt-4 border-t border-slate-200 flex flex-wrap gap-3">
            <button
              onClick={() => navigate(`/investigation/${result.investigation_id}`)}
              className="px-4 py-2 rounded-md bg-blue-600 hover:bg-blue-700 text-white font-medium text-xs transition-colors flex items-center gap-2 shadow-xs"
            >
              <FileText className="w-4 h-4" />
              Open Full Investigation Viewer &rarr;
            </button>
            <button
              onClick={() => navigate(`/investigation/${result.investigation_id}?tab=report`)}
              className="px-4 py-2 rounded-md bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 font-medium text-xs transition-colors shadow-xs"
            >
              View 10-Section Report
            </button>
            <button
              onClick={() => navigate(`/investigation/${result.investigation_id}?tab=verdict`)}
              className="px-4 py-2 rounded-md bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 font-medium text-xs transition-colors shadow-xs"
            >
              View Deliberation Trace
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
