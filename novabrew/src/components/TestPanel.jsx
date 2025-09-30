import { useState } from 'react';
import { testLlamaConnection } from '../services/llamaService';

function TestPanel() {
  const [testResult, setTestResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const runTest = async () => {
    setLoading(true);
    const result = await testLlamaConnection();
    setTestResult(result);
    setLoading(false);
  };

  return (
    <div className="test-panel">
      <h2>System Test Panel</h2>
      <button
        onClick={runTest}
        disabled={loading}
        className="test-button"
      >
        {loading ? 'Testing...' : 'Test Llama Connection'}
      </button>

      {testResult && (
        <div className={`test-result ${testResult.success ? 'success' : 'error'}`}>
          {testResult.success ? (
            <p>✅ Connection Successful: {testResult.response}</p>
          ) : (
            <p>❌ Connection Failed: {testResult.error}</p>
          )}
        </div>
      )}
    </div>
  );
}

export default TestPanel;