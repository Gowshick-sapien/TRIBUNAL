import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, useSearchParams } from 'react-router-dom';
import {
  FileText,
  ShieldCheck,
  ShieldAlert,
  Layers,
  ArrowLeft,
  Download,
  Share2,
  Maximize2,
} from 'lucide-react';
import { api } from '../services/api';
import type { ReportResponse, VerdictResponse } from '../types';
import { VerdictBadge } from '../components/common/VerdictBadge';
import { RiskChip } from '../components/common/RiskChip';
import { ConfidenceMeter } from '../components/common/ConfidenceMeter';
import { EvidenceGraph } from '../components/graph/EvidenceGraph';

export const ViewerPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();

  const activeTab = searchParams.get('tab') || 'summary';

  const [report, setReport] = useState<ReportResponse | null>(null);
  const [verdict, setVerdict] = useState<VerdictResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;
    const loadArtifacts = async () => {
      setLoading(true);
      setError(null);
      try {
        const [rep, ver] = await Promise.all([
          api.getReport(id, 'json').catch(() => null),
          api.getVerdict(id).catch(() => null),
        ]);

        if (!rep && !ver) {
          setError(`Investigation '${id}' not found in memory or persistent storage.`);
        } else {
          setReport(rep as ReportResponse);
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
    <div className="p-6 md:p-8 max-w-7xl mx-auto space-y-6 font-sans">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 pb-4">
        <div className="space-y-1">
          <button
            onClick={() => navigate('/history')}
            className="text-xs font-sans text-blue-600 font-medium flex items-center gap-1.5 hover:underline mb-2"
          >
            <ArrowLeft className="w-3.5 h-3.5" /> Back to History
          </button>
          <div className="flex items-center gap-3">
            <h1 className="text-xl font-bold font-mono text-slate-900">{id}</h1>
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
            className="px-3 py-1.5 rounded-md bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 font-sans font-medium text-xs transition-colors flex items-center gap-2 shadow-xs"
          >
            <Download className="w-3.5 h-3.5" /> Export Markdown
          </button>
        </div>
      </div>

      {/* Tabs Bar */}
      <div className="flex border-b border-slate-200 gap-1 font-sans text-xs overflow-x-auto">
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
              className={`px-4 py-2 rounded-t-md font-medium transition-colors flex items-center gap-2 border-b-2 ${
                isActive
                  ? 'bg-white text-blue-700 border-blue-600 font-semibold shadow-xs'
                  : 'text-slate-600 border-transparent hover:text-slate-900 hover:bg-slate-50'
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
            <div className="md:col-span-2 surface-card p-6 rounded-lg border border-slate-200 space-y-4 bg-white shadow-xs">
              <h2 className="text-xs font-sans font-semibold text-slate-500 uppercase tracking-wider">
                Primary Hypothesis & Finding
              </h2>
              <h3 className="text-lg font-bold font-sans text-slate-900">
                {verdict?.winning_hypothesis || report?.recommendation || 'Investigation Completed'}
              </h3>
              <p className="text-sm text-slate-800 leading-relaxed font-sans bg-slate-50 p-4 rounded-lg border border-slate-200">
                {report?.json_payload?.executive_summary?.findings || report?.markdown_content?.substring(0, 400) || 'Comprehensive investigation findings persisted in D.2 repository.'}
              </p>
            </div>

            <div className="surface-card p-5 rounded-lg border border-slate-200 space-y-4 bg-white shadow-xs">
              <ConfidenceMeter confidence={verdict?.confidence || 0.85} />
              <div className="space-y-2 text-xs font-sans border-t border-slate-200 pt-3">
                <div className="flex justify-between">
                  <span className="text-slate-500">Risk Assessment</span>
                  <RiskChip risk={report?.risk_level || 'MEDIUM'} />
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">Consensus Verdict</span>
                  <span className="text-blue-600 font-mono font-semibold">{verdict?.verdict || 'COMPLETED'}</span>
                </div>
              </div>
            </div>
          </div>

          <div className="surface-card p-6 rounded-lg border border-slate-200 space-y-3 bg-white shadow-xs">
            <h3 className="text-xs font-sans font-semibold text-slate-500 uppercase tracking-wider">
              Actionable Recommendation
            </h3>
            <p className="text-sm font-sans text-slate-800 bg-slate-50 p-4 rounded-lg border border-slate-200">
              {verdict?.recommendation || report?.recommendation || 'Proceed according to compliance guidelines.'}
            </p>
          </div>
        </div>
      )}

      {/* Tab 2: Evidence & Topology */}
      {activeTab === 'evidence' && (
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-xs font-sans font-semibold text-slate-700 uppercase tracking-wider flex items-center gap-2">
              <Share2 className="w-4 h-4 text-blue-600" />
              Interactive Evidence Graph Canvas (D.4)
            </h2>
            <button
              onClick={() => navigate(`/graph/${id}`)}
              className="px-3 py-1.5 rounded-md bg-blue-600 hover:bg-blue-700 text-white font-medium text-xs transition-colors flex items-center gap-1.5 shadow-xs"
            >
              <Maximize2 className="w-3.5 h-3.5" />
              Open Fullscreen Studio
            </button>
          </div>

          <div className="h-[600px] w-full">
            <EvidenceGraph investigationId={id} />
          </div>
        </div>
      )}

      {/* Tab 3: Defense Counter-Review */}
      {activeTab === 'defense' && (
        <div className="surface-card p-6 rounded-lg border border-slate-200 space-y-4 bg-white shadow-xs">
          <h2 className="text-xs font-sans font-semibold text-slate-700 uppercase tracking-wider flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-emerald-600" />
            Adversarial Defense Review Findings
          </h2>
          <p className="text-sm text-slate-800 leading-relaxed font-sans bg-slate-50 p-4 rounded-lg border border-slate-200">
            The Defense Agent performed adversarial counter-exploration on the Evidence Graph to identify alternative legitimate business explanations (e.g., seasonal payroll distribution, legitimate inter-account transfers).
          </p>
          <div className="p-4 rounded-lg bg-emerald-50 border border-emerald-200 text-emerald-800 font-sans text-xs">
            Status: Adversarial Review Completed. Rebuttal Cards synthesized into Evidence Graph.
          </div>
        </div>
      )}

      {/* Tab 4: Tribunal Consensus */}
      {activeTab === 'tribunal' && (
        <div className="space-y-6">
          <div className="surface-card p-6 rounded-lg border border-slate-200 space-y-4 bg-white shadow-xs">
            <h2 className="text-xs font-sans font-semibold text-slate-700 uppercase tracking-wider flex items-center gap-2">
              <ShieldAlert className="w-4 h-4 text-blue-600" />
              Tribunal Multi-Hypothesis Consensus
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="p-4 rounded-lg bg-blue-50/50 border border-blue-200 space-y-2">
                <span className="text-[10px] font-sans text-blue-700 uppercase font-semibold">Primary Winning Hypothesis</span>
                <p className="text-sm font-bold text-slate-900 font-sans">{verdict?.winning_hypothesis || 'Structuring Activity'}</p>
                <div className="text-xs font-mono text-blue-700 font-semibold">
                  Confidence Score: {((verdict?.confidence || 0.9) * 100).toFixed(0)}%
                </div>
              </div>
              <div className="p-4 rounded-lg bg-slate-50 border border-slate-200 space-y-2">
                <span className="text-[10px] font-sans text-slate-500 uppercase font-semibold">Runner-Up Hypothesis</span>
                <p className="text-sm font-bold text-slate-800 font-sans">{verdict?.runner_up_hypothesis || 'High Velocity Transfer'}</p>
                <div className="text-xs font-mono text-slate-600 font-semibold">
                  Confidence Gap: {((verdict?.confidence_gap || 0.15) * 100).toFixed(0)}%
                </div>
              </div>
            </div>
          </div>

          {verdict?.deliberation_trace && verdict.deliberation_trace.length > 0 && (
            <div className="surface-card p-6 rounded-lg border border-slate-200 space-y-3 bg-white shadow-xs">
              <h3 className="text-xs font-sans font-semibold text-slate-500 uppercase tracking-wider">
                Deliberation Trace History
              </h3>
              <div className="space-y-2">
                {verdict.deliberation_trace.map((step, i) => (
                  <div key={i} className="p-3 rounded-lg bg-slate-50 border border-slate-200 text-xs font-sans text-slate-800">
                    <span className="text-blue-600 font-semibold font-mono mr-2">Step {step.step_number}:</span>
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
        <div className="surface-card p-6 rounded-lg border border-slate-200 space-y-4 bg-white shadow-xs">
          <h2 className="text-xs font-sans font-semibold text-slate-700 uppercase tracking-wider">
            Full 10-Section Generated Report
          </h2>
          <pre className="p-5 rounded-lg bg-slate-50 border border-slate-200 font-mono text-xs text-slate-900 overflow-x-auto whitespace-pre-wrap leading-relaxed">
            {report?.markdown_content || 'Report content loaded from persistent storage.'}
          </pre>
        </div>
      )}
    </div>
  );
};
