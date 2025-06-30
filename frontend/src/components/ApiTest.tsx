import React, { useEffect, useState } from 'react';
import { checkBackendHealth } from '../services/testApi';

const ApiTest: React.FC = () => {
  const [result, setResult] = useState<any>(null);

  useEffect(() => {
    checkBackendHealth().then(setResult);
  }, []);

  return (
    <div style={{ margin: '2rem', padding: '1rem', border: '1px solid #ccc', borderRadius: '8px' }}>
      <h3>Backend Health Check</h3>
      <pre>{JSON.stringify(result, null, 2)}</pre>
    </div>
  );
};

export default ApiTest; 