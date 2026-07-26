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
    <div className="surface-card rounded-md p-1 border border-slate-200 flex items-center gap-1 shadow-xs bg-white font-sans text-xs">
      <button
        onClick={onZoomIn}
        className="p-1.5 rounded-md text-slate-600 hover:text-slate-900 hover:bg-slate-50 transition-colors"
        title="Zoom In"
      >
        <ZoomIn className="w-4 h-4" />
      </button>

      <button
        onClick={onZoomOut}
        className="p-1.5 rounded-md text-slate-600 hover:text-slate-900 hover:bg-slate-50 transition-colors"
        title="Zoom Out"
      >
        <ZoomOut className="w-4 h-4" />
      </button>

      <button
        onClick={onFitView}
        className="p-1.5 rounded-md text-slate-600 hover:text-slate-900 hover:bg-slate-50 transition-colors"
        title="Fit to Screen"
      >
        <Maximize2 className="w-4 h-4" />
      </button>

      <button
        onClick={onReset}
        className="p-1.5 rounded-md text-slate-600 hover:text-slate-900 hover:bg-slate-50 transition-colors"
        title="Reset View"
      >
        <RotateCcw className="w-4 h-4" />
      </button>

      <div className="w-px h-4 bg-slate-200 mx-1" />

      {/* Winning Path Toggle Button */}
      <button
        onClick={onToggleWinningPath}
        className={`px-2.5 py-1 rounded-md font-sans text-xs font-medium transition-colors flex items-center gap-1.5 border shadow-xs ${
          showWinningPathOnly
            ? 'bg-blue-600 text-white border-blue-600'
            : 'bg-white border-slate-200 text-slate-700 hover:bg-slate-50'
        }`}
        title="Highlight Tribunal Winning Reasoning Chain"
      >
        <Award className="w-3.5 h-3.5" />
        {showWinningPathOnly ? 'Winning Chain Active' : 'Highlight Winning Chain'}
      </button>

      <div className="w-px h-4 bg-slate-200 mx-1" />

      <button
        onClick={onExportPng}
        className="p-1.5 rounded-md text-slate-600 hover:text-slate-900 hover:bg-slate-50 transition-colors flex items-center gap-1 text-xs font-sans font-medium"
        title="Export Graph to PNG Image"
      >
        <Download className="w-4 h-4 text-slate-600" />
        <span className="hidden sm:inline">PNG</span>
      </button>
    </div>
  );
};
