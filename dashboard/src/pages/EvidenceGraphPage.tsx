import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Layers } from 'lucide-react';
import { EvidenceGraph } from '../components/graph/EvidenceGraph';

export const EvidenceGraphPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  if (!id) {
    return (
      <div className="p-8 text-center text-slate-500 font-mono text-sm">
        Invalid Investigation ID.
      </div>
    );
  }

  return (
    <div className="h-[calc(100vh-4rem)] p-6 flex flex-col space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-3 shrink-0">
        <div className="flex items-center gap-3">
          <button
            onClick={() => navigate(`/investigation/${id}`)}
            className="text-xs font-mono text-cyan-400 flex items-center gap-1.5 hover:underline"
          >
            <ArrowLeft className="w-3.5 h-3.5" /> Back to Investigation
          </button>
          <div className="h-4 w-px bg-slate-800" />
          <h1 className="text-lg font-bold font-mono text-slate-100 flex items-center gap-2">
            <Layers className="w-5 h-5 text-cyan-400" />
            Interactive Evidence Graph Studio — {id}
          </h1>
        </div>
      </div>

      {/* Fullscreen Graph Canvas */}
      <div className="flex-1 min-h-0">
        <EvidenceGraph investigationId={id} />
      </div>
    </div>
  );
};
