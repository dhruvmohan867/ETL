import { useState, useEffect } from 'react';
import api from '../api/client';

export default function SuspiciousPage() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [reviewingId, setReviewingId] = useState(null);
  const [reviewerName, setReviewerName] = useState('');
  const [notes, setNotes] = useState('');

  const fetchRecords = () => {
    setLoading(true);
    api.get('emissions/', { params: { is_suspicious: 'true' } })
      .then((res) => setRecords(res.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  };

  useEffect(() => { fetchRecords(); }, []);

  const handleReview = async (recordId, decision) => {
    if (!reviewerName.trim()) return;

    try {
      await api.post('reviews/', {
        emission_record: recordId,
        decision: decision,
        reviewer_name: reviewerName,
        notes: notes,
      });
      setReviewingId(null);
      setNotes('');
      fetchRecords();
    } catch (err) {
      alert('Review failed: ' + (err.response?.data?.error || 'Unknown error'));
    }
  };

  if (loading) {
    return <div className="text-slate-400">Loading suspicious records...</div>;
  }

  const pendingRecords = records.filter((r) => r.status === 'pending');
  const reviewedRecords = records.filter((r) => r.status !== 'pending');

  return (
    <div>
      <h1 className="text-2xl font-bold text-white mb-6">Suspicious Records</h1>

      {!reviewerName && (
        <div className="bg-slate-800 rounded-xl border border-slate-700 p-5 mb-6 max-w-md">
          <label className="block text-sm text-slate-300 mb-2">Your Name (for reviews)</label>
          <input
            type="text"
            placeholder="Enter reviewer name"
            onBlur={(e) => setReviewerName(e.target.value)}
            className="w-full bg-slate-900 border border-slate-600 text-white rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-emerald-500"
          />
        </div>
      )}

      {pendingRecords.length === 0 ? (
        <div className="text-slate-400 bg-slate-800 rounded-xl p-6 border border-slate-700">
          No suspicious records pending review.
        </div>
      ) : (
        <div className="bg-slate-800 rounded-xl border border-slate-700 overflow-hidden mb-8">
          <div className="p-4 border-b border-slate-700">
            <h2 className="text-lg font-semibold text-amber-400">{pendingRecords.length} Pending Review</h2>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="text-slate-400 border-b border-slate-700 bg-slate-900/50">
                <tr>
                  <th className="p-3">ID</th>
                  <th className="p-3">Source</th>
                  <th className="p-3">Category</th>
                  <th className="p-3">Value</th>
                  <th className="p-3">Unit</th>
                  <th className="p-3">Date</th>
                  <th className="p-3">Reason</th>
                  <th className="p-3">Actions</th>
                </tr>
              </thead>
              <tbody>
                {pendingRecords.map((r) => (
                  <tr key={r.id} className="border-b border-slate-700/50 text-slate-300">
                    <td className="p-3 text-white font-mono">#{r.id}</td>
                    <td className="p-3">{r.source_type}</td>
                    <td className="p-3">{r.category}</td>
                    <td className="p-3">{r.raw_value}</td>
                    <td className="p-3">{r.raw_unit || '—'}</td>
                    <td className="p-3">{r.reporting_date}</td>
                    <td className="p-3 text-amber-400 text-xs max-w-xs">{r.suspicious_reason}</td>
                    <td className="p-3">
                      {reviewingId === r.id ? (
                        <div className="flex flex-col gap-2 min-w-[200px]">
                          <textarea
                            value={notes}
                            onChange={(e) => setNotes(e.target.value)}
                            placeholder="Notes (optional)"
                            rows={2}
                            className="bg-slate-900 border border-slate-600 text-white text-xs rounded px-2 py-1 focus:outline-none"
                          />
                          <div className="flex gap-2">
                            <button
                              onClick={() => handleReview(r.id, 'approved')}
                              className="px-3 py-1 bg-emerald-600 hover:bg-emerald-500 text-white text-xs rounded font-medium transition-colors"
                            >
                              Approve
                            </button>
                            <button
                              onClick={() => handleReview(r.id, 'rejected')}
                              className="px-3 py-1 bg-red-600 hover:bg-red-500 text-white text-xs rounded font-medium transition-colors"
                            >
                              Reject
                            </button>
                            <button
                              onClick={() => { setReviewingId(null); setNotes(''); }}
                              className="px-3 py-1 bg-slate-700 hover:bg-slate-600 text-white text-xs rounded transition-colors"
                            >
                              Cancel
                            </button>
                          </div>
                        </div>
                      ) : (
                        <button
                          onClick={() => setReviewingId(r.id)}
                          disabled={!reviewerName}
                          className="px-3 py-1 bg-blue-600 hover:bg-blue-500 disabled:bg-slate-700 disabled:cursor-not-allowed text-white text-xs rounded font-medium transition-colors"
                        >
                          Review
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {reviewedRecords.length > 0 && (
        <div className="bg-slate-800 rounded-xl border border-slate-700 overflow-hidden">
          <div className="p-4 border-b border-slate-700">
            <h2 className="text-lg font-semibold text-slate-300">{reviewedRecords.length} Already Reviewed</h2>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="text-slate-400 border-b border-slate-700 bg-slate-900/50">
                <tr>
                  <th className="p-3">ID</th>
                  <th className="p-3">Source</th>
                  <th className="p-3">Category</th>
                  <th className="p-3">Reason</th>
                  <th className="p-3">Status</th>
                </tr>
              </thead>
              <tbody>
                {reviewedRecords.map((r) => (
                  <tr key={r.id} className="border-b border-slate-700/50 text-slate-300">
                    <td className="p-3 font-mono">#{r.id}</td>
                    <td className="p-3">{r.source_type}</td>
                    <td className="p-3">{r.category}</td>
                    <td className="p-3 text-xs">{r.suspicious_reason}</td>
                    <td className="p-3">
                      <span className={`px-2 py-1 rounded text-xs font-medium ${
                        r.status === 'approved' ? 'bg-emerald-900/50 text-emerald-400' : 'bg-red-900/50 text-red-400'
                      }`}>
                        {r.status}
                      </span>
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
