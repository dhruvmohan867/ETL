import { useState } from 'react';
import api from '../api/client';

const SOURCE_OPTIONS = [
  { value: 'sap_fuel', label: 'SAP Fuel / Procurement' },
  { value: 'utility', label: 'Utility Electricity' },
  { value: 'travel', label: 'Travel Platform' },
];

export default function UploadPage() {
  const [sourceType, setSourceType] = useState('sap_fuel');
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;

    setUploading(true);
    setResult(null);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await api.post(`uploads/${sourceType}/`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setResult(res.data);
      setFile(null);
      e.target.reset();
    } catch (err) {
      setError(err.response?.data?.error || 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div>
      <h1 className="text-2xl font-bold text-white mb-6">Upload Data Source</h1>

      <form onSubmit={handleUpload} className="bg-slate-800 rounded-xl p-6 border border-slate-700 max-w-lg">
        <div className="mb-5">
          <label className="block text-sm font-medium text-slate-300 mb-2">Source Type</label>
          <select
            value={sourceType}
            onChange={(e) => setSourceType(e.target.value)}
            className="w-full bg-slate-900 border border-slate-600 text-white rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-emerald-500"
          >
            {SOURCE_OPTIONS.map((opt) => (
              <option key={opt.value} value={opt.value}>{opt.label}</option>
            ))}
          </select>
        </div>

        <div className="mb-5">
          <label className="block text-sm font-medium text-slate-300 mb-2">CSV File</label>
          <input
            type="file"
            accept=".csv"
            onChange={(e) => setFile(e.target.files[0])}
            className="w-full text-slate-300 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-emerald-600 file:text-white file:font-medium file:cursor-pointer hover:file:bg-emerald-500"
          />
        </div>

        <button
          type="submit"
          disabled={!file || uploading}
          className="w-full bg-emerald-600 hover:bg-emerald-500 disabled:bg-slate-600 disabled:cursor-not-allowed text-white font-semibold py-2.5 rounded-lg transition-colors"
        >
          {uploading ? 'Processing...' : 'Upload & Process'}
        </button>
      </form>

      {result && (
        <div className="mt-6 bg-emerald-900/30 border border-emerald-700 rounded-xl p-5 max-w-lg">
          <h3 className="text-emerald-400 font-semibold mb-3">Upload Successful</h3>
          <div className="grid grid-cols-2 gap-3 text-sm">
            <div className="text-slate-400">File</div>
            <div className="text-white">{result.file_name}</div>
            <div className="text-slate-400">Rows Processed</div>
            <div className="text-white">{result.rows_processed}</div>
            <div className="text-slate-400">Suspicious Rows</div>
            <div className={result.suspicious_count > 0 ? 'text-amber-400' : 'text-emerald-400'}>
              {result.suspicious_count}
            </div>
          </div>
        </div>
      )}

      {error && (
        <div className="mt-6 bg-red-900/30 border border-red-700 rounded-xl p-5 max-w-lg">
          <p className="text-red-400">{error}</p>
        </div>
      )}
    </div>
  );
}
