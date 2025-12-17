import React from 'react';
import './CompanyDetails.css';

function CompanyDetails({ data }) {
  const downloadSummary = () => {
    const summary = {
      domain: data.domain,
      company_name: data.company_name,
      short_description: data.short_description,
      long_description: data.long_description,
      industry: data.industry,
      sub_industry: data.sub_industry,
      sector: data.sector,
      sic_code: data.sic_code,
      sic_text: data.sic_text,
      tags: data.tags
    };

    const blob = new Blob([JSON.stringify(summary, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${data.domain}_summary.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const downloadCSV = () => {
    const csvRows = [
      ['Field', 'Value'],
      ['Domain', data.domain],
      ['Company Name', data.company_name],
      ['Short Description', data.short_description || ''],
      ['Long Description', data.long_description || ''],
      ['Industry', data.industry || ''],
      ['Sub Industry', data.sub_industry || ''],
      ['Sector', data.sector || ''],
      ['SIC Code', data.sic_code || ''],
      ['SIC Text', data.sic_text || ''],
      ['Tags', data.tags || '']
    ];

    const csvContent = csvRows.map(row => 
      row.map(cell => `"${String(cell).replace(/"/g, '""')}"`).join(',')
    ).join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${data.domain}_details.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const sections = [
    {
      title: 'Company Overview',
      icon: '🏢',
      fields: [
        { label: 'Company Name', value: data.company_name, highlight: true },
        { label: 'Domain', value: data.domain },
        { label: 'Short Description', value: data.short_description },
        { label: 'Long Description', value: data.long_description, fullWidth: true }
      ]
    },
    {
      title: 'Industry Classification',
      icon: '📊',
      fields: [
        { label: 'Industry', value: data.industry, highlight: true },
        { label: 'Sub Industry', value: data.sub_industry },
        { label: 'Sector', value: data.sector },
        { label: 'SIC Code', value: data.sic_code },
        { label: 'SIC Description', value: data.sic_text, fullWidth: true }
      ]
    },
    {
      title: 'Tags & Keywords',
      icon: '🏷️',
      fields: [
        { label: 'Tags', value: data.tags, fullWidth: true }
      ]
    }
  ];

  return (
    <div className="company-details-container">
      <div className="details-header">
        <h2>{data.company_name || data.domain}</h2>
        <div className="download-buttons">
          <button onClick={downloadSummary} className="download-btn">
            Download Summary (JSON)
          </button>
          <button onClick={downloadCSV} className="download-btn">
            Download Details (CSV)
          </button>
        </div>
      </div>

      <div className="details-content">
        {sections.map((section, idx) => (
          <div key={idx} className="details-section">
            <div className="section-header">
              <span className="section-icon">{section.icon}</span>
              <h3 className="section-title">{section.title}</h3>
            </div>
            <div className="fields-container">
              {section.fields.map((field, fieldIdx) => (
                <div 
                  key={fieldIdx} 
                  className={`field-item ${field.fullWidth ? 'full-width' : ''} ${field.highlight ? 'highlight' : ''}`}
                >
                  <label className="field-label">{field.label}</label>
                  <div className="field-value">
                    {field.value || <span className="empty-value">Not available</span>}
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default CompanyDetails;

