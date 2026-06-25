import React, { useState } from 'react';
import './App.css';
import DomainInput from './components/DomainInput';
import CompanyDetails from './components/CompanyDetails';
import GraphVisualization from './components/GraphVisualization';
import LoadingSpinner from './components/LoadingSpinner';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

function App() {
  const [companyData, setCompanyData] = useState(null);
  const [graphData, setGraphData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleDomainSubmit = async (domain) => {
    setLoading(true);
    setError(null);
    setCompanyData(null);
    setGraphData(null);

    try {
      // Fetch company data
      const response = await fetch(`${API_BASE_URL}/api/lookup?domain=${encodeURIComponent(domain)}`);
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to fetch company data');
      }

      const data = await response.json();
      
      // Validate that we have actual company data
      // Check if domain exists and we have meaningful data
      if (!data.domain || (!data.company_name && !data.short_description)) {
        throw new Error(`No data found for domain: ${domain}. Please check if the domain exists in the offline sites folder.`);
      }
      
      setCompanyData(data);

      // Fetch graph data
      try {
        const graphResponse = await fetch(`${API_BASE_URL}/api/graph/${encodeURIComponent(domain)}`);
        if (graphResponse.ok) {
          const graph = await graphResponse.json();
          // Validate graph data
          if (graph && graph.nodes && graph.nodes.length > 0) {
            setGraphData(graph);
          }
        }
      } catch (graphError) {
        console.warn('Graph data not available:', graphError);
      }

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="app-header">
        <h1>Company Intelligence Dashboard</h1>
        <p>Extract and visualize company information from domains</p>
      </header>

      <main className="app-main">
        <DomainInput onSubmit={handleDomainSubmit} disabled={loading} />

        {loading && <LoadingSpinner />}

        {error && (
          <div className="error-message">
            <h3>Error</h3>
            <p>{error}</p>
          </div>
        )}

        {companyData && (
          <>
            <CompanyDetails data={companyData} />
            {graphData && <GraphVisualization graphData={graphData} />}
          </>
        )}
      </main>
    </div>
  );
}

export default App;

