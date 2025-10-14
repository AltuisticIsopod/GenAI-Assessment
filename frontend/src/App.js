import React, { useState } from 'react';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);
    setError(null);
    setResults(null);
  };

  const parseFile = async () => {
    if (!selectedFile) return;
    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      const response = await axios.post(`${API_BASE_URL}/upload`, formData);
      setResults({ type: 'parse', data: response.data });
    } catch (error) {
      setError(`Parse failed: ${error.response?.data?.message || error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const analyzeFile = async () => {
    if (!selectedFile) return;
    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      const response = await axios.post(`${API_BASE_URL}/analyze`, formData);
      setResults({ type: 'analysis', data: response.data });
    } catch (error) {
      setError(`Analysis failed: ${error.response?.data?.detail || error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const clearAll = () => {
    setSelectedFile(null);
    setResults(null);
    setError(null);
    document.getElementById('fileInput').value = '';
  };

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1 style={{ textAlign: 'center', color: '#333', marginBottom: '30px' }}>
        Excel Data Analyzer
      </h1>

      <div style={{ border: '2px dashed #ccc', padding: '20px', textAlign: 'center', marginBottom: '20px' }}>
        <input
          type="file"
          id="fileInput"
          accept=".xlsx,.xls"
          onChange={handleFileSelect}
          style={{ marginBottom: '10px' }}
        />
        {selectedFile && (
          <p style={{ color: '#666', fontSize: '14px' }}>
            Selected: {selectedFile.name} ({(selectedFile.size / 1024).toFixed(1)} KB)
          </p>
        )}
      </div>

      <div style={{ textAlign: 'center', marginBottom: '20px' }}>
        <button
          onClick={parseFile}
          disabled={!selectedFile || loading}
          style={{
            padding: '10px 20px',
            margin: '0 10px',
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: selectedFile && !loading ? 'pointer' : 'not-allowed',
            opacity: selectedFile && !loading ? 1 : 0.6
          }}
        >
          Parse Excel
        </button>
        <button
          onClick={analyzeFile}
          disabled={!selectedFile || loading}
          style={{
            padding: '10px 20px',
            margin: '0 10px',
            backgroundColor: '#28a745',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: selectedFile && !loading ? 'pointer' : 'not-allowed',
            opacity: selectedFile && !loading ? 1 : 0.6
          }}
        >
          AI Analysis
        </button>
        <button
          onClick={clearAll}
          disabled={loading}
          style={{
            padding: '10px 20px',
            margin: '0 10px',
            backgroundColor: '#6c757d',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: loading ? 'not-allowed' : 'pointer',
            opacity: loading ? 0.6 : 1
          }}
        >
          Clear
        </button>
      </div>

      {loading && (
        <div style={{ textAlign: 'center', padding: '20px' }}>
          <div style={{ 
            border: '4px solid #f3f3f3',
            borderTop: '4px solid #007bff',
            borderRadius: '50%',
            width: '40px',
            height: '40px',
            animation: 'spin 1s linear infinite',
            margin: '0 auto 10px'
          }}></div>
          Processing...
        </div>
      )}

      {error && (
        <div style={{
          backgroundColor: '#f8d7da',
          color: '#721c24',
          padding: '15px',
          borderRadius: '4px',
          marginBottom: '20px',
          border: '1px solid #f5c6cb'
        }}>
          {error}
        </div>
      )}

      {results && (
        <div style={{ marginTop: '20px' }}>
          <h3 style={{ color: '#333', marginBottom: '10px' }}>
            {results.type === 'parse' ? 'Parse Results' : 'AI Analysis Results'}
          </h3>
          <div style={{
            backgroundColor: '#f8f9fa',
            border: '1px solid #dee2e6',
            borderRadius: '4px',
            padding: '15px',
            maxHeight: '400px',
            overflow: 'auto'
          }}>
            <pre style={{ margin: 0, fontSize: '12px', whiteSpace: 'pre-wrap' }}>
              {JSON.stringify(results.data, null, 2)}
            </pre>
          </div>
        </div>
      )}

      <style>{`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}

export default App;
