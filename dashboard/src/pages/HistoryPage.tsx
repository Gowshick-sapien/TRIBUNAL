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
    <div className="p-6 md:p-8 max-w-7xl mx-auto space-y-6 font-sans">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 pb-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 font-sans tracking-tight flex items-center gap-2">
            <Database className="w-5 h-5 text-blue-600" />
            Persistent Investigation Repository Browser
          </h1>
          <p className="text-xs font-sans text-slate-500 mt-1">
            Browse, inspect, and manage historical persistent investigations backed by SQLite metadata & filesystem storage (D.2).
          </p>
        </div>

        <button
          onClick={loadHistory}
          className="px-3 py-1.5 rounded-md bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 font-sans font-medium text-xs transition-colors flex items-center gap-2 shadow-xs shrink-0"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          Refresh List
        </button>
      </div>

      {/* Filter Controls */}
      <div className="surface-card p-4 rounded-lg border border-slate-200 flex flex-col md:flex-row gap-4 justify-between bg-white shadow-xs">
        <div className="relative flex-1">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5 pointer-events-none" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search by ID, query text, or intent..."
            className="w-full bg-white border border-slate-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 rounded-md py-1.5 pl-9 pr-3 text-xs font-sans text-slate-900 placeholder-slate-400"
          />
        </div>

        <div className="flex items-center gap-2">
          <Filter className="w-4 h-4 text-slate-400" />
          <span className="text-xs font-sans text-slate-600 font-medium">Risk Filter:</span>
          <select
            value={riskFilter}
            onChange={(e) => setRiskFilter(e.target.value)}
            className="bg-white border border-slate-200 focus:border-blue-500 rounded-md py-1.5 px-3 text-xs font-sans text-slate-900"
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
      <div className="surface-card rounded-lg border border-slate-200 overflow-hidden shadow-xs bg-white">
        {loading ? (
          <div className="p-12 text-center text-slate-500 font-sans text-xs">
            Loading investigation records from SQLite storage...
          </div>
        ) : filtered.length === 0 ? (
          <div className="p-12 text-center text-slate-600 font-sans text-xs space-y-2">
            <p className="font-medium text-slate-800">No historical investigations found matching criteria.</p>
            <p className="text-slate-500">Run an investigation in the workspace to create new persistent records.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-slate-50 border-b border-slate-200 text-[10px] font-sans font-semibold uppercase tracking-wider text-slate-500">
                  <th className="py-3 px-4">Case ID</th>
                  <th className="py-3 px-4">Query / Objective</th>
                  <th className="py-3 px-4">Dataset</th>
                  <th className="py-3 px-4">Risk & Verdict</th>
                  <th className="py-3 px-4">Confidence</th>
                  <th className="py-3 px-4">Duration</th>
                  <th className="py-3 px-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-xs font-sans">
                {filtered.map((inv) => (
                  <tr
                    key={inv.id}
                    onClick={() => navigate(`/investigation/${inv.id}`)}
                    className="hover:bg-slate-50/80 transition-colors cursor-pointer group"
                  >
                    <td className="py-3.5 px-4 font-mono font-semibold text-blue-600 whitespace-nowrap">
                      {inv.id}
                    </td>
                    <td className="py-3.5 px-4 font-sans text-slate-900 max-w-xs truncate">
                      {inv.query}
                    </td>
                    <td className="py-3.5 px-4 text-slate-600 font-mono text-[11px] whitespace-nowrap">
                      {inv.dataset}
                    </td>
                    <td className="py-3.5 px-4 whitespace-nowrap">
                      <div className="flex items-center gap-2">
                        <RiskChip risk={inv.risk_level} />
                      </div>
                    </td>
                    <td className="py-3.5 px-4 w-32">
                      <ConfidenceMeter confidence={inv.confidence} showLabel={false} />
                      <span className="text-[10px] font-mono text-slate-500 mt-1 block">
                        {(inv.confidence * 100).toFixed(0)}%
                      </span>
                    </td>
                    <td className="py-3.5 px-4 text-slate-600 whitespace-nowrap font-mono text-[11px]">
                      {inv.duration_ms ? `${inv.duration_ms.toFixed(0)} ms` : '—'}
                    </td>
                    <td className="py-3.5 px-4 text-right whitespace-nowrap">
                      <div className="flex items-center justify-end gap-2">
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            navigate(`/investigation/${inv.id}`);
                          }}
                          className="p-1.5 rounded-md bg-white border border-slate-200 text-slate-500 hover:text-blue-600 hover:border-blue-300 transition-colors shadow-xs"
                          title="Open Viewer"
                        >
                          <ExternalLink className="w-3.5 h-3.5" />
                        </button>
                        <button
                          onClick={(e) => handleDelete(e, inv.id)}
                          className="p-1.5 rounded-md bg-white border border-slate-200 text-slate-400 hover:text-rose-600 hover:border-rose-300 transition-colors shadow-xs"
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
