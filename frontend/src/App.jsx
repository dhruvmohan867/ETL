import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom';
import UploadPage from './pages/UploadPage';
import DashboardPage from './pages/DashboardPage';
import SuspiciousPage from './pages/SuspiciousPage';
import AuditLogPage from './pages/AuditLogPage';

const NAV_ITEMS = [
  { path: '/', label: 'Dashboard', icon: '📊' },
  { path: '/upload', label: 'Upload', icon: '📤' },
  { path: '/suspicious', label: 'Suspicious', icon: '⚠️' },
  { path: '/audit-log', label: 'Audit Trail', icon: '📋' },
];

export default function App() {
  return (
    <BrowserRouter>
      <div className="flex h-screen bg-slate-950">
        <aside className="w-60 bg-slate-900 border-r border-slate-800 flex flex-col">
          <div className="p-5 border-b border-slate-800">
            <h1 className="text-lg font-bold text-emerald-400 tracking-tight">BreatheESG</h1>
            <p className="text-xs text-slate-500 mt-0.5">Ingestion Platform</p>
          </div>
          <nav className="flex-1 p-3">
            {NAV_ITEMS.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                end={item.path === '/'}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-4 py-2.5 rounded-lg mb-1 text-sm font-medium transition-colors ${
                    isActive
                      ? 'bg-emerald-600/20 text-emerald-400'
                      : 'text-slate-400 hover:text-white hover:bg-slate-800'
                  }`
                }
              >
                <span>{item.icon}</span>
                <span>{item.label}</span>
              </NavLink>
            ))}
          </nav>
        </aside>
        <main className="flex-1 overflow-auto p-8">
          <Routes>
            <Route path="/" element={<DashboardPage />} />
            <Route path="/upload" element={<UploadPage />} />
            <Route path="/suspicious" element={<SuspiciousPage />} />
            <Route path="/audit-log" element={<AuditLogPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}
