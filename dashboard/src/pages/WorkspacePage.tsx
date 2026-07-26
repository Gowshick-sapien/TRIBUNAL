import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import {
  Play,
  Database,
  Sparkles,
  ShieldAlert,
  FileText,
  CheckCircle,
  ExternalLink,
  RotateCcw,
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
    const loadDatasets = async () => {
      try {
        const data = await api.getDatasets();
        if (data.datasets && data.datasets.length > 0) {
          setAvailableDatasets(data.datasets);
        }
      } catch {
        // Fallback default
      }
    };
    loadDatasets();
  }, [location.state]);

  const handleRunInvestigation = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);

    // Reset steps
    setSteps((prev) =>
      prev.map((s) => ({
        ...s,
        status: 'pending',
        durationMs: undefined,
      }))
    );

    try {
      // Simulate pipeline execution animation steps
      setSteps((prev) =>
        prev.map((s) => (s.id === '1' ? { ...s, status: 'running' } : s))
      );

      setTimeout(() => {
        setSteps((prev) =>
          prev.map((s) =>
            s.id === '1'
              ? { ...s, status: 'completed', durationMs: 12.5 }
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
              ? { ...s, status: 'completed', durationMs: 18.2 }
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
              ? { ...s, status: 'completed', durationMs: 15.0 }
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

      // Complete all steps
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
    <div className="p-6 md:p-8 max-w-7xl mx-auto space-y-8 font-sans">
      {/* Page Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 pb-6">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-xl md:text-2xl font-bold text-slate-900 tracking-tight font-sans">
              Investigation Execution Workspace
            </h1>
            <span className="px-2 py-0.5 text-[10px] font-mono font-medium bg-blue-50 border border-blue-200 text-blue-700 rounded-md">
              D.1 Rest API
            </span>
          </div>
          <p className="text-slate-600 text-xs font-sans mt-1">
            Orchestrate end-to-end multi-expert analysis, adversarial defense review, and tribunal consensus.
          </p>
        </div>
      </div>

      {/* Query Input Section */}
      <div className="surface-card p-6 rounded-lg border border-slate-200 space-y-6 bg-white shadow-xs">
        <form onSubmit={handleRunInvestigation} className="space-y-4">
          <div className="space-y-2">
            <label className="block text-xs font-sans font-semibold text-slate-900 uppercase tracking-wider">
              Natural Language Investigation Query / Objective
            </label>
            <div className="relative">
              <textarea
                rows={3}
                disabled={loading}
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="e.g. Is customer ACC_8000A94C0 engaged in structuring and velocity anomalies?"
                className="w-full p-3.5 bg-slate-50 border border-slate-200 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 rounded-lg text-sm text-slate-900 placeholder-slate-400 font-sans transition-colors resize-none disabled:opacity-50"
              />
            </div>
          </div>

          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pt-2">
            <div className="flex items-center gap-3">
              <Database className="w-4 h-4 text-slate-400" />
              <span className="text-xs font-sans font-medium text-slate-700">Target Dataset:</span>
              <select
                disabled={loading}
                value={dataset}
                onChange={(e) => setDataset(e.target.value)}
                className="px-3 py-1.5 bg-white border border-slate-200 rounded-md text-xs font-sans text-slate-800 font-medium focus:outline-none focus:border-blue-500"
              >
                {availableDatasets.map((d) => (
                  <option key={d.id} value={d.id}>
                    {d.name}
                  </option>
                ))}
              </select>
            </div>

            <button
              type="submit"
              disabled={loading || !query.trim()}
              className="px-6 py-2.5 rounded-md bg-blue-600 hover:bg-blue-700 disabled:bg-slate-300 text-white font-medium text-xs transition-colors flex items-center justify-center gap-2 shadow-xs"
            >
              {loading ? (
                <>
                  <Sparkles className="w-4 h-4 animate-spin" />
                  Orchestrating Investigation Pipeline...
                </>
              ) : (
                <>
                  <Play className="w-4 h-4 fill-current" />
                  Execute Autonomous Investigation
                </>
              )}
            </button>
          </div>
        </form>
      </div>

      {/* Execution Progress & Status */}
      {(loading || steps.some((s) => s.status !== 'pending')) && (
        <ExecutionTimeline steps={steps} totalMs={result?.metrics?.total_ms} />
      )}

      {/* Domain Guard Rejection & Error View */}
      {error && (
        <div className="surface-card p-6 rounded-lg border border-amber-200 bg-amber-50/70 space-y-4 font-sans shadow-xs">
          <div className="flex items-start gap-3">
            <div className="p-2.5 rounded-lg bg-amber-100 text-amber-800 shrink-0">
              <ShieldAlert className="w-5 h-5" />
            </div>
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <h3 className="text-sm font-bold text-slate-900 font-sans">
                  Investigation Domain Guard Rejection (Phase C.1.1)
                </h3>
                <span className="px-2 py-0.5 text-[10px] font-mono font-medium bg-amber-200/80 text-amber-900 rounded">
                  Out-of-Domain Query
                </span>
              </div>
              <p className="text-xs text-slate-800 leading-relaxed font-sans font-medium">
                {error}
              </p>
            </div>
          </div>

          <div className="pt-3 border-t border-amber-200/60 space-y-2">
            <span className="text-[11px] font-sans font-semibold text-slate-700 uppercase tracking-wider">
              Try Supported AML Investigation Objectives:
            </span>
            <div className="flex flex-wrap gap-2">
              {[
                { label: 'Structuring & Velocity', q: 'Is customer ACC_8000A94C0 engaged in structuring and velocity anomalies?' },
                { label: 'Behavioral Baseline Drift', q: 'Check account ACC_9999B11C1 for dormancy reactivation and currency change drift' },
                { label: 'Customer Account Lookup', q: 'Investigate ACC_8016B3750' },
              ].map((item, idx) => (
                <button
                  key={idx}
                  onClick={() => {
                    setQuery(item.q);
                    setError(null);
                  }}
                  className="px-3 py-1 rounded-md bg-white border border-slate-200 hover:border-blue-300 hover:bg-blue-50/50 text-slate-700 text-xs font-sans transition-colors"
                >
                  {item.label} &rarr;
                </button>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Investigation Results Card */}
      {result && (
        <div className="surface-card p-6 rounded-lg border border-slate-200 space-y-6 bg-white shadow-xs font-sans">
          {/* Header */}
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 pb-4">
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <span className="text-xs text-slate-500 font-medium">Case ID:</span>
                <button
                  onClick={() => navigate(`/report/${result.investigation_id}`)}
                  className="font-mono text-sm font-bold text-blue-600 hover:underline flex items-center gap-1 group"
                  title="Open 10-Section Interactive Report"
                >
                  <span>{result.investigation_id}</span>
                  <ExternalLink className="w-3.5 h-3.5 text-blue-500 opacity-70 group-hover:opacity-100" />
                </button>
                <span className="text-[10px] font-sans bg-emerald-50 border border-emerald-200 text-emerald-700 px-2 py-0.5 rounded-md flex items-center gap-1 font-medium">
                  <CheckCircle className="w-3 h-3" /> Persisted to Storage (D.2)
                </span>
              </div>
              <h2 className="text-lg font-bold text-slate-900 font-sans flex items-center gap-2 pt-1">
                <span>Autonomous Investigation Completed</span>
              </h2>
            </div>

            <div className="flex items-center gap-3">
              <VerdictBadge verdict={result.verdict} size="lg" />
              <RiskChip risk={result.risk_level} />
            </div>
          </div>

          {/* Structured Concept Breakdown: Requested Target vs Suspicious Entity */}
          {(() => {
            const suspectMatch = result.winning_hypothesis?.match(/(?:Account|Customer)\s+([A-Za-z0-9_-]+)/i);
            const suspectEntity = suspectMatch ? suspectMatch[1] : null;
            const targetQuery = result.query;

            return (
              <div className="grid grid-cols-1 sm:grid-cols-4 gap-4 bg-slate-50/80 p-4 rounded-lg border border-slate-200">
                <div>
                  <div className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">Investigation Target</div>
                  <div className="text-sm font-bold text-slate-900 font-mono mt-0.5 bg-white px-2 py-1 rounded border border-slate-200 inline-block">
                    {targetQuery}
                  </div>
                </div>
                <div>
                  <div className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">Primary Suspicious Entity</div>
                  <div className="text-sm font-bold text-blue-700 font-mono mt-0.5 bg-blue-50/80 px-2 py-1 rounded border border-blue-200 inline-block">
                    {suspectEntity ? `Account ${suspectEntity}` : 'Target Account'}
                  </div>
                </div>
                <div className="sm:col-span-2">
                  <div className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">Primary Typology Finding</div>
                  <div className="text-xs font-semibold text-slate-800 mt-1 leading-relaxed">
                    {result.winning_hypothesis}
                  </div>
                </div>
              </div>
            );
          })()}

          {/* Metrics & Confidence */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="md:col-span-2 space-y-3">
              <div className="text-xs font-sans font-semibold text-slate-700 uppercase tracking-wider">
                Executive Findings Summary
              </div>
              <p className="text-sm text-slate-800 leading-relaxed font-sans bg-slate-50/50 p-4 rounded-lg border border-slate-200">
                {result.summary}
              </p>
              <p className="text-xs text-slate-800 font-sans bg-slate-50/50 p-3 rounded-lg border border-slate-200">
                <strong className="text-slate-900">Actionable Recommendation:</strong> {result.recommendation}
              </p>
            </div>

            <div className="surface-card p-4 rounded-lg border border-slate-200 space-y-4 flex flex-col justify-between bg-white">
              <ConfidenceMeter confidence={result.confidence} />

              <div className="space-y-2 text-xs font-sans border-t border-slate-200 pt-3">
                <div className="flex justify-between">
                  <span className="text-slate-500">Total Latency</span>
                  <span className="text-blue-600 font-mono font-semibold">{result.metrics?.total_ms?.toFixed(1) || '0.0'} ms</span>
                </div>
              </div>
            </div>
          </div>

          {/* Action Links */}
          <div className="pt-4 border-t border-slate-200 flex flex-wrap items-center justify-between gap-3">
            <div className="flex flex-wrap items-center gap-3">
              <button
                onClick={() => navigate(`/report/${result.investigation_id}`)}
                className="px-4 py-2.5 rounded-md bg-blue-600 hover:bg-blue-700 text-white font-medium text-xs transition-colors flex items-center gap-2 shadow-xs"
              >
                <FileText className="w-4 h-4" />
                Open 10-Section Investigation Report &rarr;
              </button>
              <button
                onClick={() => navigate(`/investigation/${result.investigation_id}`)}
                className="px-4 py-2.5 rounded-md bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 font-medium text-xs transition-colors shadow-xs"
              >
                View Interactive Case File
              </button>
              <button
                onClick={() => navigate(`/investigation/${result.investigation_id}?tab=verdict`)}
                className="px-4 py-2.5 rounded-md bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 font-medium text-xs transition-colors shadow-xs"
              >
                View Deliberation Trace
              </button>
            </div>

            <button
              onClick={() => {
                setResult(null);
                setQuery('');
                window.scrollTo({ top: 0, behavior: 'smooth' });
              }}
              className="px-4 py-2.5 rounded-md bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium text-xs transition-colors flex items-center gap-1.5 shadow-xs"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              Run Another Investigation
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
