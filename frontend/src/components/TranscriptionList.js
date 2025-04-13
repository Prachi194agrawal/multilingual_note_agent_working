import React from 'react';
import './TranscriptionList.css';

const TranscriptionList = ({ transcriptions, onSelect, selectedId }) => {
  return (
    <div className="transcription-list">
      <h3>Your Recordings</h3>
      {transcriptions.length === 0 ? (
        <p className="no-transcriptions">No recordings found</p>
      ) : (
        <ul>
          {transcriptions.map((item) => (
            <li 
              key={item.id} 
              className={selectedId === item.id ? 'selected' : ''}
              onClick={() => onSelect(item.id)}
            >
              <div className="transcription-item">
                <span className="transcription-title">{item.filename}</span>
                <div className="transcription-info">
                  <span className="language-tag">
                    {item.language === 'en' ? 'English' : 
                     item.language === 'zh' ? 'Chinese' : 
                     item.language === 'yue' ? 'Cantonese' : 
                     item.language}
                  </span>
                  <span className="transcription-date">
                    {new Date(item.created_at).toLocaleDateString()}
                  </span>
                </div>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default TranscriptionList;