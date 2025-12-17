import React, { useState } from 'react';
import './DomainInput.css';

function DomainInput({ onSubmit, disabled }) {
  const [domain, setDomain] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (domain.trim() && !disabled) {
      onSubmit(domain.trim());
    }
  };

  return (
    <div className="domain-input-container">
      <form onSubmit={handleSubmit} className="domain-form">
        <div className="input-group">
          <label htmlFor="domain">Enter Domain Name</label>
          <div className="input-wrapper">
            <input
              id="domain"
              type="text"
              value={domain}
              onChange={(e) => setDomain(e.target.value)}
              placeholder="e.g., airbnb.com, spotify.com"
              disabled={disabled}
              className="domain-input"
            />
            <button
              type="submit"
              disabled={disabled || !domain.trim()}
              className="submit-button"
            >
              {disabled ? 'Processing...' : 'Analyze'}
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}

export default DomainInput;


