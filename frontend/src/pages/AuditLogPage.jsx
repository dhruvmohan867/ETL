import { useState, useEffect } from 'react';
import api from '../api/client';

const ACTION_LABELS = {
  upload: 'File Upload',
  review_approve: 'Approved',
  review_reject: 'Rejected',
};

const ACTION_COLORS = {
  upload: 'bg-blue-900/50 text-blue-400',
  review_approve: 'bg-emerald-900/50 text-emerald-400',
  review_reject: 'bg-red-900/50 text-red-400',
};

export default function AuditLogPage() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('audit-logs/')
      .then((res) => setLogs(res.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div className="text-slate-400">Loading audit log...</div>;
  }

  return (
    <div>
      <h1 className="text-2xl font-bold text-white mb-6">Audit Trail</h1>

      {logs.length === 0 ? (
        <div className="text-slate-400 bg-slate-800 rounded-xl p-6 border border-slate-700">
          No audit entries yet.
        </div>
      ) : (
        <div className="bg-slate-800 rounded-xl border border-slate-700 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="text-slate-400 border-b border-slate-700 bg-slate-900/50">
                <tr>
                  <th className="p-3">Timestamp</th>
                  <th className="p-3">Action</th>
                  <th className="p-3">Target</th>
                  <th className="p-3">Performed By</th>
                  <th className="p-3">Details</th>
                </tr>
              </thead>
              <tbody>
                {logs.map((log) => (
                  <tr key={log.id} className="border-b border-slate-700/50 text-slate-300">
                    <td className="p-3 text-xs whitespace-nowrap">
                      {new Date(log.created_at).toLocaleString()}
                    </td>
                    <td className="p-3">
                      <span className={`px-2 py-1 rounded text-xs font-medium ${ACTION_COLORS[log.action] || 'bg-slate-700 text-slate-300'}`}>
                        {ACTION_LABELS[log.action] || log.action}
                      </span>
                    </td>
                    <td className="p-3 font-mono text-xs">{log.target_type} #{log.target_id}</td>
                    <td className="p-3">{log.performed_by}</td>
                    <td className="p-3 text-xs text-slate-400 max-w-xs truncate">
                      {log.details && typeof log.details === 'object'
                        ? Object.entries(log.details).map(([k, v]) => `${k}: ${v}`).join(', ')
                        : String(log.details)
                      }
                    </td>
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
