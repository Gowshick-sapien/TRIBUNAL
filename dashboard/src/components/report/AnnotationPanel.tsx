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
    <div className="fixed inset-y-0 right-0 w-full sm:w-[400px] z-50 bg-white border-l border-slate-200 p-6 overflow-y-auto space-y-6 shadow-2xl font-sans no-print">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-200 pb-4 font-sans">
        <div className="flex items-center gap-2">
          <MessageSquare className="w-4.5 h-4.5 text-amber-600" />
          <span className="font-semibold text-slate-900 text-sm">Investigator Annotations</span>
        </div>
        <button
          onClick={onClose}
          className="p-1.5 rounded-md bg-white border border-slate-200 text-slate-500 hover:text-slate-900 hover:bg-slate-50 transition-colors"
        >
          <X className="w-4 h-4" />
        </button>
      </div>

      <p className="text-xs font-sans text-slate-500 leading-relaxed">
        Attach review notes to Case <strong className="text-blue-600 font-mono font-semibold">{reportId}</strong>. Annotations are stored independently without mutating the immutable investigation report.
      </p>

      {/* Form */}
      <form onSubmit={handleSubmit} className="space-y-3 font-sans text-xs">
        <div>
          <label className="text-[10px] text-slate-500 uppercase font-semibold block mb-1">Author / Role</label>
          <input
            type="text"
            value={author}
            onChange={(e) => setAuthor(e.target.value)}
            className="w-full bg-white border border-slate-200 rounded-md p-2 text-slate-900 font-sans"
          />
        </div>
        <div>
          <label className="text-[10px] text-slate-500 uppercase font-semibold block mb-1">Note Annotation</label>
          <textarea
            rows={3}
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="e.g. Needs SAR review for velocity anomaly..."
            className="w-full bg-white border border-slate-200 rounded-md p-2 text-slate-900 placeholder-slate-400 font-sans text-xs"
          />
        </div>
        <button
          type="submit"
          disabled={!text.trim()}
          className="w-full py-2 rounded-md bg-amber-600 hover:bg-amber-700 text-white font-medium transition-colors flex items-center justify-center gap-1.5 disabled:opacity-40 shadow-xs"
        >
          <Send className="w-3.5 h-3.5" /> Attach Annotation
        </button>
      </form>

      {/* List */}
      <div className="space-y-3 pt-4 border-t border-slate-200 font-sans text-xs">
        <span className="text-[10px] text-slate-500 uppercase font-semibold block">
          Attached Annotations ({annotations.length})
        </span>

        {annotations.length === 0 ? (
          <div className="text-slate-400 text-center py-6 text-xs font-sans">No annotations attached yet.</div>
        ) : (
          annotations.map((note) => (
            <div key={note.id} className="p-3.5 rounded-lg bg-slate-50 border border-slate-200 space-y-2">
              <div className="flex items-center justify-between text-[11px]">
                <span className="font-semibold text-amber-700 font-sans">{note.author}</span>
                <button
                  onClick={() => onDeleteAnnotation(note.id)}
                  className="text-slate-400 hover:text-rose-600 transition-colors"
                  title="Remove Annotation"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                </button>
              </div>
              <p className="text-slate-800 font-sans text-xs leading-relaxed">{note.text}</p>
              <span className="text-[10px] text-slate-400 font-mono block">
                {new Date(note.created_at).toLocaleString()}
              </span>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
