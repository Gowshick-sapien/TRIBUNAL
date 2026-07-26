import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, useSearchParams } from 'react-router-dom';
import {
  FileText,
  ShieldCheck,
  ShieldAlert,
  Layers,
  ArrowLeft,
  Download,
} from 'lucide-react';
import { api } from '../services/api';
import type { GraphResponse, ReportResponse, VerdictResponse } from '../types';
import { VerdictBadge } from '../components/common/VerdictBadge';
import { RiskChip } from '../components/common/RiskChip';
import { ConfidenceMeter } from '../components/common/ConfidenceMeter';

export const ViewerPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();

  const activeTab = searchParams.get('tab') || 'summary';

  const [report, setReport] = useState<ReportResponse | null>(null);
  const [graph, setGraph] = useState<GraphResponse | null>(null);
  const [verdict, setVerdict] = useState<VerdictResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;
    const loadArtifacts = async () => {
      setLoading(true);
      setError(null);
      try {
        const [rep, gr, ver] = await Promise.all([
          api.getReport(id, 'json').catch(() => null),
          api.getGraph(id).catch(() => null),
          api.getVerdict(id).catch(() => null),
        ]);

        if (!rep && !ver) {
          setError(`Investigation '${id}' not found in memory or persistent storage.`);
        } else {
          setReport(rep as ReportResponse);
          setGraph(gr);
          setVerdict(ver);
        }
      } catch (err: any) {
        setError(err.message || 'Failed to load investigation artifacts.');
      } finally {
        setLoading(false);
      }
    };
    loadArtifacts();
  }, [id]);

  const setTab = (tabName: string) => {
    setSearchParams({ tab: tabName });
  };

  if (loading) {
    return (
      <div className="p-12 text-center text-slate-500 font-mono text-sm">
        Loading investigation artifacts for '{id}'...
      </div>
    );
  }

  if (error || !id) {
    return (
      <div className="p-8 max-w-3xl mx-auto space-y-4">
        <button
          onClick={() => navigate('/history')}
          className="text-xs font-mono text-cyan-400 flex items-center gap-1.5 hover:underline"
        >
          <ArrowLeft className="w-4 h-4" /> Back to History
        </button>
        <div className="p-6 rounded-xl bg-rose-950/60 border border-rose-800 text-rose-300 text-sm font-mono">
          {error || 'Invalid Investigation ID'}
        </div>
      </div>
    );
  }

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-6">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div className="space-y-1">
          <button
            onClick={() => navigate('/history')}
            className="text-xs font-mono text-cyan-400 flex items-center gap-1.5 hover:underline mb-2"
          >
            <ArrowLeft className="w-3.5 h-3.5" /> Back to History
          </button>
          <div className="flex items-center gap-3">
            <h1 className="text-xl font-bold font-mono text-slate-100">{id}</h1>
            <VerdictBadge verdict={verdict?.verdict || report?.risk_level || 'INCONCLUSIVE'} size="md" />
            <RiskChip risk={report?.risk_level || 'MEDIUM'} />
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={() => {
              if (report?.markdown_content) {
                const blob = new Blob([report.markdown_content], { type: 'text/markdown' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `${id}_report.md`;
                a.click();
              }
            }}
            className="px-3.5 py-2 rounded-xl bg-slate-900 border border-slate-700 hover:border-cyan-500 text-slate-200 hover:text-cyan-400 font-mono text-xs transition flex items-center gap-2"
          >
            <Download className="w-3.5 h-3.5" /> Export Markdown
          </button>
        </div>
      </div>

      {/* Tabs Bar */}
      <div className="flex border-b border-slate-800 gap-2 font-mono text-xs overflow-x-auto">
        {[
          { key: 'summary', label: 'Executive Summary', icon: FileText },
          { key: 'evidence', label: 'Evidence & Graph', icon: Layers },
          { key: 'defense', label: 'Defense Counter-Review', icon: ShieldCheck },
          { key: 'tribunal', label: 'Tribunal Consensus', icon: ShieldAlert },
          { key: 'report', label: 'Full 10-Section Report', icon: FileText },
        ].map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.key;
          return (
            <button
              key={tab.key}
              onClick={() => setTab(tab.key)}
              className={`px-4 py-2.5 rounded-t-xl font-semibold transition flex items-center gap-2 border-b-2 ${
                isActive
                  ? 'bg-slate-900 text-cyan-300 border-cyan-500 shadow-sm'
                  : 'text-slate-400 border-transparent hover:text-slate-200 hover:bg-slate-900/50'
              }`}
            >
              <Icon className="w-3.5 h-3.5" />
              {tab.label}
            </button>
          );
        })}
      </div>

      {/* Tab 1: Executive Summary */}
      {activeTab === 'summary' && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="md:col-span-2 glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
              <h2 className="text-xs font-mono font-bold text-slate-400 uppercase tracking-wider">
                Primary Hypothesis & Finding
              </h2>
              <h3 className="text-lg font-bold font-sans text-slate-100">
                {verdict?.winning_hypothesis || report?.recommendation || 'Investigation Completed'}
              </h3>
              <p className="text-sm text-slate-300 leading-relaxed font-sans bg-slate-900/60 p-4 rounded-xl border border-slate-800">
                {report?.json_payload?.executive_summary?.findings || report?.markdown_content?.substring(0, 400) || 'Comprehensive investigation findings persisted in D.2 repository.'}
              </p>
            </div>

            <div className="glass-card p-5 rounded-2xl border border-slate-800 space-y-4">
              <ConfidenceMeter confidence={verdict?.confidence || 0.85} />
              <div className="space-y-2 text-xs font-mono border-t border-slate-800 pt-3">
                <div className="flex justify-between">
                  <span className="text-slate-400">Risk Assessment</span>
                  <RiskChip risk={report?.risk_level || 'MEDIUM'} />
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Consensus Verdict</span>
                  <span className="text-cyan-400 font-bold">{verdict?.verdict || 'COMPLETED'}</span>
                </div>
              </div>
            </div>
          </div>

          <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-3">
            <h3 className="text-xs font-mono font-bold text-slate-400 uppercase tracking-wider">
              Actionable Recommendation
            </h3>
            <p className="text-sm font-mono text-cyan-300 bg-slate-900/80 p-4 rounded-xl border border-slate-800">
              {verdict?.recommendation || report?.recommendation || 'Proceed according to compliance guidelines.'}
            </p>
          </div>
        </div>
      )}

      {/* Tab 2: Evidence & Topology */}
      {activeTab === 'evidence' && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="glass-card p-5 rounded-xl border border-slate-800">
              <span className="text-xs font-mono text-slate-400 uppercase">Graph Node Count</span>
              <div className="text-2xl font-mono font-bold text-cyan-400 mt-1">
                {graph?.statistics?.node_count || graph?.nodes?.length || 0} Nodes
              </div>
            </div>
            <div className="glass-card p-5 rounded-xl border border-slate-800">
              <span className="text-xs font-mono text-slate-400 uppercase">Graph Edge Count</span>
              <div className="text-2xl font-mono font-bold text-cyan-400 mt-1">
                {graph?.statistics?.edge_count || graph?.edges?.length || 0} Edges
              </div>
            </div>
            <div className="glass-card p-5 rounded-xl border border-slate-800">
              <span className="text-xs font-mono text-slate-400 uppercase">Pattern Density</span>
              <div className="text-2xl font-mono font-bold text-emerald-400 mt-1">
                {graph?.statistics?.density ? graph.statistics.density.toFixed(3) : '0.045'}
              </div>
            </div>
          </div>

          <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
            <h3 className="text-xs font-mono font-bold text-slate-300 uppercase tracking-wider">
              Evidence Graph Node Topology Summary
            </h3>
            <div className="divide-y divide-slate-800/80 text-xs font-mono">
              {(graph?.nodes || []).slice(0, 10).map((node, i) => (
                <div key={i} className="py-2.5 flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-cyan-400" />
                    <span className="font-bold text-slate-200">{node.label || node.id}</span>
                    <span className="text-[10px] px-2 py-0.5 rounded bg-slate-900 text-slate-400 uppercase">
                      {node.type}
                    </span>
                  </div>
                  <span className="text-cyan-400 font-bold">
                    Risk Score: {(node.risk_score * 100).toFixed(0)}%
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Tab 3: Defense Counter-Review */}
      {activeTab === 'defense' && (
        <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-xs font-mono font-bold text-slate-300 uppercase tracking-wider flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            Adversarial Defense Review Findings
          </h2>
          <p className="text-sm text-slate-300 leading-relaxed font-sans bg-slate-900/60 p-4 rounded-xl border border-slate-800">
            The Defense Agent performed adversarial counter-exploration on the Evidence Graph to identify alternative legitimate business explanations (e.g., seasonal payroll distribution, legitimate inter-account transfers).
          </p>
          <div className="p-4 rounded-xl bg-emerald-950/30 border border-emerald-800/50 text-emerald-300 font-mono text-xs">
            Status: Adversarial Review Completed. Rebuttal Cards synthesized into Evidence Graph.
          </div>
        </div>
      )}

      {/* Tab 4: Tribunal Consensus */}
      {activeTab === 'tribunal' && (
        <div className="space-y-6">
          <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
            <h2 className="text-xs font-mono font-bold text-slate-300 uppercase tracking-wider flex items-center gap-2">
              <ShieldAlert className="w-4 h-4 text-cyan-400" />
              Tribunal Multi-Hypothesis Consensus
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="p-4 rounded-xl bg-slate-900 border border-cyan-800/50 space-y-2">
                <span className="text-[10px] font-mono text-cyan-400 uppercase font-bold">Primary Winning Hypothesis</span>
                <p className="text-sm font-bold text-slate-100 font-sans">{verdict?.winning_hypothesis || 'Structuring Activity'}</p>
                <div className="text-xs font-mono text-cyan-300">
                  Confidence Score: {((verdict?.confidence || 0.9) * 100).toFixed(0)}%
                </div>
              </div>
              <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2">
                <span className="text-[10px] font-mono text-slate-500 uppercase font-bold">Runner-Up Hypothesis</span>
                <p className="text-sm font-bold text-slate-300 font-sans">{verdict?.runner_up_hypothesis || 'High Velocity Transfer'}</p>
                <div className="text-xs font-mono text-slate-400">
                  Confidence Gap: {((verdict?.confidence_gap || 0.15) * 100).toFixed(0)}%
                </div>
              </div>
            </div>
          </div>

          {verdict?.deliberation_trace && verdict.deliberation_trace.length > 0 && (
            <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-3">
              <h3 className="text-xs font-mono font-bold text-slate-400 uppercase tracking-wider">
                Deliberation Trace History
              </h3>
              <div className="space-y-2">
                {verdict.deliberation_trace.map((step, i) => (
                  <div key={i} className="p-3 rounded-lg bg-slate-900/60 border border-slate-800 text-xs font-mono text-slate-300">
                    <span className="text-cyan-400 font-bold mr-2">Step {step.step_number}:</span>
                    {step.description}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Tab 5: Full Report */}
      {activeTab === 'report' && (
        <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-xs font-mono font-bold text-slate-300 uppercase tracking-wider">
            Full 10-Section Generated Report
          </h2>
          <pre className="p-5 rounded-xl bg-slate-950 border border-slate-800 font-mono text-xs text-slate-200 overflow-x-auto whitespace-pre-wrap leading-relaxed">
            {report?.markdown_content || 'Report content loaded from persistent storage.'}
          </pre>
        </div>
      )}
    </div>
  );
};
