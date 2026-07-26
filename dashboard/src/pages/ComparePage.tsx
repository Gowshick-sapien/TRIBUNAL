import React, { useEffect, useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import { searchApi } from '../services/search_api';
import type { SearchResultItem } from '../types/search';
import { ComparisonPanel } from '../components/search/ComparisonPanel';

export const ComparePage: React.FC = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  const leftId = searchParams.get('left') || searchParams.get('a') || '';
  const rightId = searchParams.get('right') || searchParams.get('b') || '';

  const [itemA, setItemA] = useState<SearchResultItem | null>(null);
  const [itemB, setItemB] = useState<SearchResultItem | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadComparisonItems = async () => {
      setLoading(true);
      try {
        const defaultFilter = {
          query: '',
          risk_level: 'ALL',
          min_confidence: 0.0,
          max_confidence: 1.0,
          dataset: 'ALL',
          status: 'ALL',
          only_bookmarked: false,
          sort_by: 'newest',
        };

        if (leftId) {
          const resA = await searchApi.search({ ...defaultFilter, query: leftId }, 50, 0);
          const foundA = resA.results.find((i) => i.id === leftId) || resA.results[0] || null;
          setItemA(foundA);
        }

        if (rightId) {
          const resB = await searchApi.search({ ...defaultFilter, query: rightId }, 50, 0);
          const foundB = resB.results.find((i) => i.id === rightId) || resB.results[0] || null;
          setItemB(foundB);
        }
      } catch (err) {
        console.error('Failed to load comparison items:', err);
      } finally {
        setLoading(false);
      }
    };

    loadComparisonItems();
  }, [leftId, rightId]);

  return (
    <div className="p-6 md:p-8 max-w-7xl mx-auto space-y-6 font-sans">
      <button
        onClick={() => navigate('/explorer')}
        className="text-xs font-sans text-blue-600 font-medium flex items-center gap-1.5 hover:underline"
      >
        <ArrowLeft className="w-3.5 h-3.5" /> Back to Repository Explorer
      </button>

      {loading ? (
        <div className="surface-card p-12 rounded-lg border border-slate-200 text-center font-sans text-xs text-slate-500 flex flex-col items-center gap-3 bg-white shadow-xs">
          <span className="w-5 h-5 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />
          Loading comparison data for {leftId || 'A'} vs {rightId || 'B'}...
        </div>
      ) : (
        <ComparisonPanel
          itemA={itemA}
          itemB={itemB}
          onNavigateViewer={(id) => navigate(`/investigation/${id}`)}
          onNavigateGraph={(id) => navigate(`/graph/${id}`)}
        />
      )}
    </div>
  );
};
