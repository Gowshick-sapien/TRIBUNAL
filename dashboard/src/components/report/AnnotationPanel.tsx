import React, { useState } from 'react';
import { X, Trash2, MessageSquare, Send } from 'lucide-react';
import type { ReportAnnotation } from '../../types/report';

interface AnnotationPanelProps {
  reportId: string;
  annotations: ReportAnnotation[];
  onAddAnnotation: (author: string, text: string) => void;
  onDeleteAnnotation: (noteId: number) => void;
  onClose: () => void;
}

export const AnnotationPanel: React.FC<AnnotationPanelProps> = ({
  reportId,
  annotations,
  onAddAnnotation,
  onDeleteAnnotation,
  onClose,
}) => {
  const [author, setAuthor] = useState('Senior Investigator');
  const [text, setText] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!text.trim()) return;
    onAddAnnotation(author, text);
    setText('');
  };

  return (
    <div className="fixed inset-y-0 right-0 w-full sm:w-[400px] z-50 glass-panel border-l border-slate-800 p-6 overflow-y-auto space-y-6 shadow-2xl animate-slideInRight backdrop-blur-xl no-print">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-4 font-mono">
        <div className="flex items-center gap-2">
          <MessageSquare className="w-5 h-5 text-amber-400" />
          <span className="font-bold text-slate-100 text-sm">Investigator Annotations</span>
        </div>
        <button
          onClick={onClose}
          className="p-1 rounded-lg bg-slate-900 text-slate-400 hover:text-slate-200 transition"
        >
          <X className="w-5 h-5" />
        </button>
      </div>

      <p className="text-xs font-mono text-slate-400 leading-relaxed">
        Attach review notes to Case <strong className="text-cyan-400">{reportId}</strong>. Annotations are stored independently without mutating the immutable investigation report.
      </p>

      {/* Form */}
      <form onSubmit={handleSubmit} className="space-y-3 font-mono text-xs">
        <div>
          <label className="text-[10px] text-slate-400 uppercase font-bold block mb-1">Author / Role</label>
          <input
            type="text"
            value={author}
            onChange={(e) => setAuthor(e.target.value)}
            className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-slate-200"
          />
        </div>
        <div>
          <label className="text-[10px] text-slate-400 uppercase font-bold block mb-1">Note Annotation</label>
          <textarea
            rows={3}
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="e.g. Needs SAR review for velocity anomaly..."
            className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-slate-200 placeholder-slate-500 font-sans text-xs"
          />
        </div>
        <button
          type="submit"
          disabled={!text.trim()}
          className="w-full py-2 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold transition flex items-center justify-center gap-1.5 disabled:opacity-40"
        >
          <Send className="w-3.5 h-3.5" /> Attach Annotation
        </button>
      </form>

      {/* List */}
      <div className="space-y-3 pt-4 border-t border-slate-800 font-mono text-xs">
        <span className="text-[10px] text-slate-500 uppercase font-bold block">
          Attached Annotations ({annotations.length})
        </span>

        {annotations.length === 0 ? (
          <div className="text-slate-500 text-center py-6 text-xs">No annotations attached yet.</div>
        ) : (
          annotations.map((note) => (
            <div key={note.id} className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 space-y-2">
              <div className="flex items-center justify-between text-[11px]">
                <span className="font-bold text-amber-400">{note.author}</span>
                <button
                  onClick={() => onDeleteAnnotation(note.id)}
                  className="text-slate-500 hover:text-rose-400 transition"
                  title="Remove Annotation"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                </button>
              </div>
              <p className="text-slate-200 font-sans text-xs">{note.text}</p>
              <span className="text-[9px] text-slate-500 block">
                {new Date(note.created_at).toLocaleString()}
              </span>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
