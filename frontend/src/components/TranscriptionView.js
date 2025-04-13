import React from 'react';
import { exportPDF } from '../utils/api';
import './TranscriptionView.css';

const TranscriptionView = ({ transcription }) => {
  if (!transcription) {
    return null;
  }

  const handleExport = () => {
    exportPDF(transcription.id);
  };

  return (
    <div className="transcription-view">
      <div className="transcription-header">
        <h2>{transcription.filename}</h2>
        <div className="transcription-meta">
          <span className="language-badge">
            {transcription.language === 'en' ? 'English' : 
             transcription.language === 'zh' ? 'Chinese' : 
             transcription.language === 'yue' ? 'Cantonese' : 
             transcription.language}
          </span>
          <span className="date-info">
            {new Date(transcription.created_at).toLocaleString()}
          </span>
        </div>
        <button className="export-button" onClick={handleExport}>
          Export as PDF
        </button>
      </div>

      <div className="summary-section">
        <h3>Summary</h3>
        <p>{transcription.summary}</p>
      </div>

      <div className="action-items-section">
        <h3>Action Items</h3>
        {transcription.action_items && transcription.action_items.length > 0 ? (
          <ul>
            {transcription.action_items.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        ) : (
          <p>No action items found</p>
        )}
      </div>

      <div className="transcript-section">
        <h3>Full Transcript</h3>
        <div className="transcript-text">
          {transcription.transcript}
        </div>
      </div>
    </div>
  );
};

export default TranscriptionView;