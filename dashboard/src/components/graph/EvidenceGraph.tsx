import React, { useMemo, useRef, useCallback } from 'react';
import {
  ReactFlow,
  Background,
  MiniMap,
  useReactFlow,
  ReactFlowProvider,
  BackgroundVariant,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { toPng } from 'html-to-image';

import { CardNode } from './nodes/CardNode';
import { TribunalNode } from './nodes/TribunalNode';
import { DefenseNode } from './nodes/DefenseNode';
import { EvidenceGapNode } from './nodes/EvidenceGapNode';
import { GraphToolbar } from './GraphToolbar';
import { GraphLegend } from './GraphLegend';
import { NodeInspector } from './NodeInspector';
import { EdgeInspector } from './EdgeInspector';
import { GraphMetrics } from './GraphMetrics';
import { SearchBar } from './SearchBar';
import { useEvidenceGraph } from '../../hooks/useEvidenceGraph';

interface EvidenceGraphInnerProps {
  investigationId: string;
}

const EvidenceGraphInner: React.FC<EvidenceGraphInnerProps> = ({ investigationId }) => {
  const reactFlowInstance = useReactFlow();
  const flowWrapperRef = useRef<HTMLDivElement>(null);

  const {
    payload,
    loading,
    error,
    nodes,
    edges,
    selectedNode,
    selectedEdge,
    setSelectedNode,
    setSelectedEdge,
    filters,
    setFilters,
  } = useEvidenceGraph(investigationId);

  // Register custom node types
  const nodeTypes = useMemo(
    () => ({
      card: CardNode,
      tribunal: TribunalNode,
      defense: DefenseNode,
      evidence_gap: EvidenceGapNode,
    }),
    []
  );

  const handleNodeClick = useCallback(
    (_: React.MouseEvent, node: any) => {
      setSelectedEdge(null);
      setSelectedNode(node.data);
    },
    [setSelectedNode, setSelectedEdge]
  );

  const handleEdgeClick = useCallback(
    (_: React.MouseEvent, edge: any) => {
      setSelectedNode(null);
      setSelectedEdge(edge.data);
    },
    [setSelectedNode, setSelectedEdge]
  );

  const handlePaneClick = useCallback(() => {
    setSelectedNode(null);
    setSelectedEdge(null);
  }, [setSelectedNode, setSelectedEdge]);

  // Export handlers
  const handleExportPng = useCallback(() => {
    if (flowWrapperRef.current === null) return;
    toPng(flowWrapperRef.current, { backgroundColor: '#ffffff', quality: 0.95 })
      .then((dataUrl) => {
        const a = document.createElement('a');
        a.download = `evidence_graph_${investigationId}.png`;
        a.href = dataUrl;
        a.click();
      })
      .catch((err) => console.error('Export PNG failed:', err));
  }, [investigationId]);

  if (loading) {
    return (
      <div className="w-full h-full surface-card rounded-lg p-12 flex flex-col items-center justify-center text-slate-500 font-sans text-xs gap-3 border border-slate-200">
        <span className="w-5 h-5 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />
        Rendering Evidence Graph canvas for '{investigationId}'...
      </div>
    );
  }

  if (error || !payload) {
    return (
      <div className="w-full h-full surface-card rounded-lg p-8 flex items-center justify-center text-rose-700 font-sans text-xs border border-rose-200 bg-rose-50">
        {error || 'Evidence Graph structure missing or unparseable.'}
      </div>
    );
  }

  return (
    <div className="w-full h-full relative flex overflow-hidden surface-card rounded-lg border border-slate-200 shadow-xs" ref={flowWrapperRef}>
      {/* Graph Canvas Workspace */}
      <div className="flex-1 h-full relative">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          nodeTypes={nodeTypes}
          onNodeClick={handleNodeClick}
          onEdgeClick={handleEdgeClick}
          onPaneClick={handlePaneClick}
          fitView
          colorMode="light"
          proOptions={{ hideAttribution: true }}
        >
          <Background color="#cbd5e1" variant={BackgroundVariant.Dots} gap={20} size={1} />
          <MiniMap
            style={{ backgroundColor: '#ffffff', border: '1px solid #cbd5e1', borderRadius: '8px' }}
            nodeColor={(n: any) => {
              if (n.type === 'tribunal') return '#2563eb';
              if (n.type === 'defense') return '#16a34a';
              return '#3b82f6';
            }}
          />
        </ReactFlow>

        {/* Top Floating Search & Filter Bar */}
        <div className="absolute top-4 left-4 z-20">
          <SearchBar filters={filters} onChange={setFilters} />
        </div>

        {/* Top Floating Toolbar */}
        <div className="absolute top-4 right-4 z-20">
          <GraphToolbar
            onZoomIn={() => reactFlowInstance.zoomIn()}
            onZoomOut={() => reactFlowInstance.zoomOut()}
            onFitView={() => reactFlowInstance.fitView()}
            onReset={() => reactFlowInstance.setViewport({ x: 0, y: 0, zoom: 1 })}
            onToggleWinningPath={() =>
              setFilters({ ...filters, showWinningPathOnly: !filters.showWinningPathOnly })
            }
            onExportPng={handleExportPng}
            showWinningPathOnly={filters.showWinningPathOnly}
          />
        </div>

        {/* Bottom Floating Legend & Metrics */}
        <div className="absolute bottom-4 left-4 z-20 flex gap-3 items-end">
          <GraphLegend />
          <GraphMetrics statistics={payload.statistics} />
        </div>
      </div>

      {/* Right Persistent Inspector Side-Panel */}
      {selectedNode && (
        <NodeInspector node={selectedNode} onClose={() => setSelectedNode(null)} />
      )}
      {selectedEdge && (
        <EdgeInspector edge={selectedEdge} onClose={() => setSelectedEdge(null)} />
      )}
    </div>
  );
};

export const EvidenceGraph: React.FC<{ investigationId: string }> = ({ investigationId }) => {
  return (
    <ReactFlowProvider>
      <EvidenceGraphInner investigationId={investigationId} />
    </ReactFlowProvider>
  );
};
