import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Navbar } from './components/layout/Navbar';
import { Sidebar } from './components/layout/Sidebar';
import { HomePage } from './pages/HomePage';
import { WorkspacePage } from './pages/WorkspacePage';
import { HistoryPage } from './pages/HistoryPage';
import { ExplorerPage } from './pages/ExplorerPage';
import { ComparePage } from './pages/ComparePage';
import { ViewerPage } from './pages/ViewerPage';
import { EvidenceGraphPage } from './pages/EvidenceGraphPage';
import { SystemPage } from './pages/SystemPage';
import { SettingsPage } from './pages/SettingsPage';

export const App: React.FC = () => {
  return (
    <Router>
      <div className="min-h-screen flex flex-col bg-[#090d16] text-slate-100 selection:bg-cyan-500/30 selection:text-cyan-200">
        <Navbar />

        <div className="flex-1 flex overflow-hidden">
          <Sidebar />

          <main className="flex-1 overflow-y-auto">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/investigate" element={<WorkspacePage />} />
              <Route path="/history" element={<HistoryPage />} />
              <Route path="/explorer" element={<ExplorerPage />} />
              <Route path="/compare" element={<ComparePage />} />
              <Route path="/investigation/:id" element={<ViewerPage />} />
              <Route path="/graph/:id" element={<EvidenceGraphPage />} />
              <Route path="/system" element={<SystemPage />} />
              <Route path="/settings" element={<SettingsPage />} />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  );
};

export default App;
