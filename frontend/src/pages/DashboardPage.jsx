import { useState, useEffect } from 'react';
import api from '../api/client';

const SOURCE_LABELS = {
  sap_fuel: 'SAP Fuel',
  utility: 'Utility',
  travel: 'Travel',
};

export default function DashboardPage() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('emissions/dashboard/')
      .then((res) => setStats(res.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div className="text-slate-400">Loading dashboard...</div>;
  }

  if (!stats) {
    return <div className="text-red-400">Failed to load dashboard data</div>;
  }

  const cards = [
    { label: 'Total Records', value: stats.total_records, color: 'bg-blue-600' },
    { label: 'Suspicious', value: stats.suspicious_count, color: 'bg-amber-600' },
    { label: 'Pending', value: stats.pending_count, color: 'bg-slate-600' },
    { label: 'Approved', value: stats.approved_count, color: 'bg-emerald-600' },
    { label: 'Rejected', value: stats.rejected_count, color: 'bg-red-600' },
  ];

  return (
    <div>
      <h1 className="text-2xl font-bold text-white mb-6">Dashboard</h1>

      <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8">
        {cards.map((card) => (
          <div key={card.label} className={`${card.color} rounded-xl p-5 text-center`}>
            <div className="text-3xl font-bold text-white">{card.value}</div>
            <div className="text-sm text-white/80 mt-1">{card.label}</div>
          </div>
        ))}
      </div>

      {stats.by_source_type.length > 0 && (
        <div className="bg-slate-800 rounded-xl border border-slate-700 p-6 mb-8">
          <h2 className="text-lg font-semibold text-white mb-4">By Source Type</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {stats.by_source_type.map((s) => (
              <div key={s.source_type} className="bg-slate-900 rounded-lg p-4 border border-slate-700">
                <div className="text-sm text-slate-400 mb-1">{SOURCE_LABELS[s.source_type] || s.source_type}</div>
                <div className="text-xl font-bold text-white">{s.total} records</div>
                {s.suspicious > 0 && (
                  <div className="text-sm text-amber-400 mt-1">{s.suspicious} suspicious</div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {stats.recent_uploads.length > 0 && (
        <div className="bg-slate-800 rounded-xl border border-slate-700 p-6">
          <h2 className="text-lg font-semibold text-white mb-4">Recent Uploads</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="text-slate-400 border-b border-slate-700">
                <tr>
                  <th className="pb-3 pr-4">File</th>
                  <th className="pb-3 pr-4">Source</th>
                  <th className="pb-3 pr-4">Company</th>
                  <th className="pb-3 pr-4">Rows</th>
                  <th className="pb-3 pr-4">Suspicious</th>
                  <th className="pb-3 pr-4">Status</th>
                  <th className="pb-3">Date</th>
                </tr>
              </thead>
              <tbody>
                {stats.recent_uploads.map((u) => (
                  <tr key={u.id} className="border-b border-slate-700/50 text-slate-300">
                    <td className="py-3 pr-4 text-white">{u.file_name}</td>
                    <td className="py-3 pr-4">{SOURCE_LABELS[u.source_type] || u.source_type}</td>
                    <td className="py-3 pr-4">{u.company_name}</td>
                    <td className="py-3 pr-4">{u.row_count}</td>
                    <td className="py-3 pr-4">
                      <span className={u.suspicious_count > 0 ? 'text-amber-400' : 'text-emerald-400'}>
                        {u.suspicious_count}
                      </span>
                    </td>
                    <td className="py-3 pr-4">
                      <span className={`px-2 py-1 rounded text-xs font-medium ${
                        u.status === 'completed' ? 'bg-emerald-900/50 text-emerald-400' :
                        u.status === 'failed' ? 'bg-red-900/50 text-red-400' :
                        'bg-slate-700 text-slate-300'
                      }`}>
                        {u.status}
                      </span>
                    </td>
                    <td className="py-3">{new Date(u.created_at).toLocaleDateString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
