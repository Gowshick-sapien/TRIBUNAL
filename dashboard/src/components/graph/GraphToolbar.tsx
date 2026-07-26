import React from 'react';
import {
  ZoomIn,
  ZoomOut,
  Maximize2,
  RotateCcw,
  Download,
  Award,
} from 'lucide-react';

interface GraphToolbarProps {
  onZoomIn: () => void;
  onZoomOut: () => void;
  onFitView: () => void;
  onReset: () => void;
  onToggleWinningPath: () => void;
  onExportPng: () => void;
  showWinningPathOnly: boolean;
}

export const GraphToolbar: React.FC<GraphToolbarProps> = ({
  onZoomIn,
  onZoomOut,
  onFitView,
  onReset,
  onToggleWinningPath,
  onExportPng,
  showWinningPathOnly,
}) => {
  return (
    <div className="glass-panel rounded-xl p-1.5 border border-slate-800 flex items-center gap-1 shadow-lg backdrop-blur-md">
      <button
        onClick={onZoomIn}
        className="p-2 rounded-lg text-slate-400 hover:text-cyan-400 hover:bg-slate-800 transition"
        title="Zoom In"
      >
        <ZoomIn className="w-4 h-4" />
      </button>

      <button
        onClick={onZoomOut}
        className="p-2 rounded-lg text-slate-400 hover:text-cyan-400 hover:bg-slate-800 transition"
        title="Zoom Out"
      >
        <ZoomOut className="w-4 h-4" />
      </button>

      <button
        onClick={onFitView}
        className="p-2 rounded-lg text-slate-400 hover:text-cyan-400 hover:bg-slate-800 transition"
        title="Fit to Screen"
      >
        <Maximize2 className="w-4 h-4" />
      </button>

      <button
        onClick={onReset}
        className="p-2 rounded-lg text-slate-400 hover:text-cyan-400 hover:bg-slate-800 transition"
        title="Reset View"
      >
        <RotateCcw className="w-4 h-4" />
      </button>

      <div className="w-px h-5 bg-slate-800 mx-1" />

      {/* Winning Path Toggle Button */}
      <button
        onClick={onToggleWinningPath}
        className={`px-3 py-1.5 rounded-lg font-mono text-xs font-bold transition flex items-center gap-1.5 ${
          showWinningPathOnly
            ? 'bg-cyan-500 text-slate-950 shadow-md shadow-cyan-500/30'
            : 'bg-slate-900 border border-slate-800 text-cyan-400 hover:bg-slate-800'
        }`}
        title="Highlight Tribunal Winning Reasoning Chain"
      >
        <Award className="w-3.5 h-3.5" />
        {showWinningPathOnly ? 'Winning Chain Active' : 'Highlight Winning Chain'}
      </button>

      <div className="w-px h-5 bg-slate-800 mx-1" />

      <button
        onClick={onExportPng}
        className="p-2 rounded-lg text-slate-400 hover:text-cyan-400 hover:bg-slate-800 transition flex items-center gap-1 text-xs font-mono"
        title="Export Graph to PNG Image"
      >
        <Download className="w-4 h-4" />
        <span className="hidden sm:inline">PNG</span>
      </button>
    </div>
  );
};
