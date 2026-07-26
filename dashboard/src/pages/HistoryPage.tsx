import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Database,
  Search,
  Trash2,
  ExternalLink,
  RefreshCw,
  Filter,
} from 'lucide-react';
import { api } from '../services/api';
import type { InvestigationRecordSchema } from '../types';
import { RiskChip } from '../components/common/RiskChip';
import { ConfidenceMeter } from '../components/common/ConfidenceMeter';

export const HistoryPage: React.FC = () => {
  const navigate = useNavigate();
  const [investigations, setInvestigations] = useState<InvestigationRecordSchema[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [riskFilter, setRiskFilter] = useState('ALL');

  const loadHistory = async () => {
    setLoading(true);
    try {
      const res = await api.listInvestigations(100, 0);
      setInvestigations(res.investigations || []);
    } catch (err) {
      console.error('Failed to load investigation history:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadHistory();
  }, []);

  const handleDelete = async (e: React.MouseEvent, id: string) => {
    e.stopPropagation();
    if (!window.confirm(`Delete investigation '${id}' from persistent storage?`)) return;

    try {
      await api.deleteInvestigation(id);
      setInvestigations((prev) => prev.filter((item) => item.id !== id));
    } catch (err) {
      alert(`Failed to delete investigation: ${err}`);
    }
  };

  const filtered = investigations.filter((inv) => {
    const matchesSearch =
      inv.id.toLowerCase().includes(search.toLowerCase()) ||
      inv.query.toLowerCase().includes(search.toLowerCase()) ||
      inv.planner_intent.toLowerCase().includes(search.toLowerCase());

    const matchesRisk = riskFilter === 'ALL' || inv.risk_level.toUpperCase() === riskFilter.toUpperCase();

    return matchesSearch && matchesRisk;
  });

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-2xl font-black text-slate-100 font-sans tracking-tight flex items-center gap-2">
            <Database className="w-6 h-6 text-cyan-400" />
            Persistent Investigation Repository Browser
          </h1>
          <p className="text-xs font-mono text-slate-400 mt-1">
            Browse, inspect, and manage historical persistent investigations backed by SQLite metadata & filesystem storage (D.2).
          </p>
        </div>

        <button
          onClick={loadHistory}
          className="px-3.5 py-2 rounded-xl bg-slate-900 border border-slate-700 hover:border-cyan-500 text-slate-300 hover:text-cyan-400 font-mono text-xs transition flex items-center gap-2"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          Refresh List
        </button>
      </div>

      {/* Filter Controls */}
      <div className="glass-panel p-4 rounded-xl border border-slate-800 flex flex-col md:flex-row gap-4 justify-between">
        <div className="relative flex-1">
          <Search className="w-4 h-4 text-slate-500 absolute left-3 top-3 pointer-events-none" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search by ID, query text, or intent..."
            className="w-full bg-slate-900 border border-slate-700 focus:border-cyan-500 rounded-lg py-2 pl-9 pr-3 text-xs font-mono text-slate-200 placeholder-slate-500"
          />
        </div>

        <div className="flex items-center gap-2">
          <Filter className="w-4 h-4 text-slate-500" />
          <span className="text-xs font-mono text-slate-400">Risk Filter:</span>
          <select
            value={riskFilter}
            onChange={(e) => setRiskFilter(e.target.value)}
            className="bg-slate-900 border border-slate-700 focus:border-cyan-500 rounded-lg py-2 px-3 text-xs font-mono text-slate-200"
          >
            <option value="ALL">ALL RISKS</option>
            <option value="CRITICAL">CRITICAL</option>
            <option value="HIGH">HIGH</option>
            <option value="MEDIUM">MEDIUM</option>
            <option value="LOW">LOW</option>
          </select>
        </div>
      </div>

      {/* Table */}
      <div className="glass-panel rounded-2xl border border-slate-800 overflow-hidden">
        {loading ? (
          <div className="p-12 text-center text-slate-500 font-mono text-xs">
            Loading investigation records from SQLite storage...
          </div>
        ) : filtered.length === 0 ? (
          <div className="p-12 text-center text-slate-400 font-mono text-xs space-y-2">
            <p>No historical investigations found matching criteria.</p>
            <p className="text-slate-500">Run an investigation in the workspace to create new persistent records.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-slate-900/90 border-b border-slate-800 text-[11px] font-mono uppercase tracking-wider text-slate-400">
                  <th className="py-3 px-4">Case ID</th>
                  <th className="py-3 px-4">Query / Objective</th>
                  <th className="py-3 px-4">Dataset</th>
                  <th className="py-3 px-4">Risk & Verdict</th>
                  <th className="py-3 px-4">Confidence</th>
                  <th className="py-3 px-4">Duration</th>
                  <th className="py-3 px-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 text-xs font-mono">
                {filtered.map((inv) => (
                  <tr
                    key={inv.id}
                    onClick={() => navigate(`/investigation/${inv.id}`)}
                    className="hover:bg-slate-800/40 transition cursor-pointer group"
                  >
                    <td className="py-3.5 px-4 font-bold text-cyan-400 whitespace-nowrap">
                      {inv.id}
                    </td>
                    <td className="py-3.5 px-4 font-sans text-slate-200 max-w-xs truncate">
                      {inv.query}
                    </td>
                    <td className="py-3.5 px-4 text-slate-400 text-[11px] whitespace-nowrap">
                      {inv.dataset}
                    </td>
                    <td className="py-3.5 px-4 whitespace-nowrap">
                      <div className="flex items-center gap-2">
                        <RiskChip risk={inv.risk_level} />
                      </div>
                    </td>
                    <td className="py-3.5 px-4 w-32">
                      <ConfidenceMeter confidence={inv.confidence} showLabel={false} />
                      <span className="text-[10px] text-slate-400 mt-1 block">
                        {(inv.confidence * 100).toFixed(0)}%
                      </span>
                    </td>
                    <td className="py-3.5 px-4 text-slate-400 whitespace-nowrap text-[11px]">
                      {inv.duration_ms ? `${inv.duration_ms.toFixed(0)} ms` : '—'}
                    </td>
                    <td className="py-3.5 px-4 text-right whitespace-nowrap">
                      <div className="flex items-center justify-end gap-2">
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            navigate(`/investigation/${inv.id}`);
                          }}
                          className="p-1.5 rounded bg-slate-900 border border-slate-700 text-slate-300 hover:text-cyan-400 hover:border-cyan-500 transition"
                          title="Open Viewer"
                        >
                          <ExternalLink className="w-3.5 h-3.5" />
                        </button>
                        <button
                          onClick={(e) => handleDelete(e, inv.id)}
                          className="p-1.5 rounded bg-slate-900 border border-slate-700 text-slate-400 hover:text-rose-400 hover:border-rose-600 transition"
                          title="Delete Persistent Record"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};
