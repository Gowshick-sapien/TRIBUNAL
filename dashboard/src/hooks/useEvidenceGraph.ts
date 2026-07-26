import { useState, useEffect, useCallback, useMemo } from 'react';
import type { Node, Edge } from '@xyflow/react';
import dagre from 'dagre';
import { graphApi } from '../services/graph_api';
import type {
  EvidenceGraphPayload,
  GraphFilterOptions,
  GraphNodeData,
  GraphEdgeData,
} from '../types/graph';

const nodeWidth = 260;
const nodeHeight = 120;

export const getDagreLayout = (
  nodes: Node<GraphNodeData>[],
  edges: Edge<GraphEdgeData>[],
  direction = 'LR'
): { nodes: Node<GraphNodeData>[]; edges: Edge<GraphEdgeData>[] } => {
  const dagreGraph = new dagre.graphlib.Graph();
  dagreGraph.setDefaultEdgeLabel(() => ({}));

  dagreGraph.setGraph({
    rankdir: direction,
    nodesep: 50,
    ranksep: 90,
  });

  nodes.forEach((node) => {
    dagreGraph.setNode(node.id, { width: nodeWidth, height: nodeHeight });
  });

  edges.forEach((edge) => {
    dagreGraph.setEdge(edge.source, edge.target);
  });

  dagre.layout(dagreGraph);

  const layoutedNodes = nodes.map((node) => {
    const nodeWithPosition = dagreGraph.node(node.id);
    return {
      ...node,
      position: {
        x: nodeWithPosition ? nodeWithPosition.x - nodeWidth / 2 : 0,
        y: nodeWithPosition ? nodeWithPosition.y - nodeHeight / 2 : 0,
      },
    };
  });

  return { nodes: layoutedNodes, edges };
};

export const useEvidenceGraph = (investigationId: string) => {
  const [payload, setPayload] = useState<EvidenceGraphPayload | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [selectedNode, setSelectedNode] = useState<GraphNodeData | null>(null);
  const [selectedEdge, setSelectedEdge] = useState<GraphEdgeData | null>(null);

  const [filters, setFilters] = useState<GraphFilterOptions>({
    expertFilter: 'ALL',
    severityFilter: 'ALL',
    relationFilter: 'ALL',
    showWinningPathOnly: false,
    searchQuery: '',
  });

  const loadGraph = useCallback(async () => {
    if (!investigationId) return;
    setLoading(true);
    setError(null);
    try {
      const data = await graphApi.getEvidenceGraph(investigationId);
      setPayload(data);
    } catch (err: any) {
      setError(err.message || 'Failed to load Evidence Graph.');
    } finally {
      setLoading(false);
    }
  }, [investigationId]);

  useEffect(() => {
    loadGraph();
  }, [loadGraph]);

  const { layoutedNodes, layoutedEdges } = useMemo(() => {
    if (!payload) return { layoutedNodes: [], layoutedEdges: [] };

    // 1. Filter Nodes
    let filteredNodes = payload.nodes.filter((node) => {
      if (filters.expertFilter !== 'ALL' && (node.expert || '').toLowerCase() !== filters.expertFilter.toLowerCase()) {
        return false;
      }
      if (filters.severityFilter !== 'ALL' && (node.severity || 'MEDIUM').toUpperCase() !== filters.severityFilter.toUpperCase()) {
        return false;
      }
      if (filters.searchQuery) {
        const q = filters.searchQuery.toLowerCase();
        const matchesId = node.id.toLowerCase().includes(q);
        const matchesHyp = (node.hypothesis || '').toLowerCase().includes(q);
        const matchesExp = (node.expert || '').toLowerCase().includes(q);
        const matchesTx = (node.transaction_ids || []).some((tx) => tx.toLowerCase().includes(q));
        if (!matchesId && !matchesHyp && !matchesExp && !matchesTx) return false;
      }
      return true;
    });

    const activeNodeIds = new Set(filteredNodes.map((n) => n.id));

    // 2. Filter Edges
    let filteredEdges = payload.edges.filter((edge) => {
      if (!activeNodeIds.has(edge.source) || !activeNodeIds.has(edge.target)) {
        return false;
      }
      if (filters.relationFilter !== 'ALL' && edge.relation !== filters.relationFilter) {
        return false;
      }
      return true;
    });

    // 3. Highlight Winning Path (Tribunal Overlay)
    if (filters.showWinningPathOnly) {
      filteredNodes = filteredNodes.map((n) => ({
        ...n,
        isDimmed: !n.isWinningPath,
      }));

      filteredEdges = filteredEdges.map((e) => ({
        ...e,
        isDimmed: !e.isWinningPath,
      }));
    } else {
      filteredNodes = filteredNodes.map((n) => ({ ...n, isDimmed: false }));
      filteredEdges = filteredEdges.map((e) => ({ ...e, isDimmed: false }));
    }

    // 4. Convert to React Flow Nodes & Edges
    const rfNodes: Node<GraphNodeData>[] = filteredNodes.map((n) => ({
      id: n.id,
      type: n.type, // registered custom node type: 'card' | 'tribunal' | 'defense' | 'evidence_gap'
      data: n,
      position: { x: 0, y: 0 },
    }));

    const rfEdges: Edge<GraphEdgeData>[] = filteredEdges.map((e) => {
      const isWinning = e.isWinningPath || e.relation === 'WINNING_PATH';
      const isContradiction = e.relation === 'CONTRADICTION';

      return {
        id: e.id,
        source: e.source,
        target: e.target,
        type: 'smoothstep',
        animated: isWinning,
        data: e,
        style: {
          stroke: isWinning ? '#38bdf8' : isContradiction ? '#f43f5e' : '#10b981',
          strokeWidth: isWinning ? 3 : 1.5,
          opacity: e.isDimmed ? 0.2 : 0.9,
        },
      };
    });

    // 5. Calculate Dagre Directional Layout
    const layout = getDagreLayout(rfNodes, rfEdges, 'LR');
    return { layoutedNodes: layout.nodes, layoutedEdges: layout.edges };
  }, [payload, filters]);

  return {
    payload,
    loading,
    error,
    nodes: layoutedNodes,
    edges: layoutedEdges,
    selectedNode,
    selectedEdge,
    setSelectedNode,
    setSelectedEdge,
    filters,
    setFilters,
    reload: loadGraph,
  };
};
