import React, { useEffect, useState, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import { reportApi } from '../services/report_api';
import type { StructuredReportPayload, ReportAnnotation } from '../types/report';
import { ReportHeader } from '../components/report/ReportHeader';
import { ReportSidebar } from '../components/report/ReportSidebar';
import { ReportToolbar } from '../components/report/ReportToolbar';
import { ExecutiveSummary } from '../components/report/ExecutiveSummary';
import { EvidenceSection } from '../components/report/EvidenceSection';
import { DefenseSection } from '../components/report/DefenseSection';
import { TribunalSection } from '../components/report/TribunalSection';
import { AuditSection } from '../components/report/AuditSection';
import { AnnotationPanel } from '../components/report/AnnotationPanel';

export const ReportViewerPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [report, setReport] = useState<StructuredReportPayload | null>(null);
  const [annotations, setAnnotations] = useState<ReportAnnotation[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeSection, setActiveSection] = useState('sec-summary');
  const [searchTerm, setSearchTerm] = useState('');
  const [showAnnotations, setShowAnnotations] = useState(false);

  const fetchReportData = useCallback(async () => {
    if (!id) return;
    setLoading(true);
    try {
      const data = await reportApi.getReport(id);
      setReport(data);
      const notes = await reportApi.getAnnotations(id);
      setAnnotations(notes);
    } catch (err) {
      console.error('Failed to load report:', err);
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    fetchReportData();
  }, [fetchReportData]);

  const handleAddAnnotation = async (author: string, text: string) => {
    if (!id) return;
    const newNote = await reportApi.addAnnotation(id, author, text);
    setAnnotations((prev) => [...prev, newNote]);
  };

  const handleDeleteAnnotation = async (noteId: number) => {
    if (!id) return;
    await reportApi.deleteAnnotation(id, noteId);
    setAnnotations((prev) => prev.filter((n) => n.id !== noteId));
  };

  const handlePrint = () => {
    window.print();
  };

  const scrollToSection = (secId: string) => {
    setActiveSection(secId);
    const el = document.getElementById(secId);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth' });
    }
  };

  if (loading || !report) {
    return (
      <div className="p-8 max-w-7xl mx-auto font-mono text-xs text-slate-500 text-center py-20">
        <span className="w-6 h-6 border-2 border-cyan-400 border-t-transparent rounded-full animate-spin inline-block mb-3" />
        <p>Loading interactive investigation report workstation for Case {id}...</p>
      </div>
    );
  }

  return (
    <div className="p-6 md:p-8 max-w-7xl mx-auto space-y-6">
      {/* Top Back Navigation */}
      <button
        onClick={() => navigate('/history')}
        className="text-xs font-mono text-cyan-400 flex items-center gap-1.5 hover:underline no-print"
      >
        <ArrowLeft className="w-3.5 h-3.5" /> Back to Investigation History
      </button>

      {/* Header */}
      <ReportHeader
        id={report.investigation_id}
        generatedAt={report.generated_at}
        riskLevel={report.risk_level}
        confidence={0.85}
        recommendation={report.recommendation}
        dataset="default"
        onNavigateGraph={() => navigate(`/graph/${report.investigation_id}`)}
        onNavigateCompare={() => navigate(`/compare?left=${report.investigation_id}`)}
        onPrint={handlePrint}
      />

      {/* Toolbar */}
      <ReportToolbar
        searchTerm={searchTerm}
        onSearchChange={(val) => setSearchTerm(val)}
        onPrint={handlePrint}
        onToggleAnnotations={() => setShowAnnotations(!showAnnotations)}
        showAnnotations={showAnnotations}
        annotationCount={annotations.length}
      />

      {/* Main Grid: Sidebar + Report Sections */}
      <div className="flex gap-6 items-start">
        <ReportSidebar
          activeSection={activeSection}
          onSelectSection={(secId) => scrollToSection(secId)}
        />

        <div className="flex-1 space-y-6 overflow-hidden">
          {/* Executive Summary */}
          <ExecutiveSummary report={report} />

          {/* Evidence Section */}
          <EvidenceSection
            onNavigateGraph={() => navigate(`/graph/${report.investigation_id}`)}
          />

          {/* Defense Section */}
          <DefenseSection />

          {/* Tribunal Section */}
          <TribunalSection />

          {/* Audit Section */}
          <AuditSection />

          {/* Markdown Full Text Backup */}
          <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-3 font-mono text-xs">
            <span className="text-slate-400 uppercase font-bold block border-b border-slate-800 pb-2">
              Full Document Text
            </span>
            <pre className="whitespace-pre-wrap font-sans text-xs text-slate-300 leading-relaxed max-h-96 overflow-y-auto p-4 bg-slate-950/60 rounded-xl border border-slate-800">
              {report.markdown_content}
            </pre>
          </div>
        </div>
      </div>

      {/* Investigator Annotations Panel */}
      {showAnnotations && (
        <AnnotationPanel
          reportId={report.investigation_id}
          annotations={annotations}
          onAddAnnotation={handleAddAnnotation}
          onDeleteAnnotation={handleDeleteAnnotation}
          onClose={() => setShowAnnotations(false)}
        />
      )}
    </div>
  );
};
