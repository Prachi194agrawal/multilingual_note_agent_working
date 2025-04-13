import React, { useState } from 'react';
import { uploadAudio } from '../utils/api';
import './UploadForm.css';

const UploadForm = ({ onUploadSuccess }) => {
  const [file, setFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    setError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!file) {
      setError('Please select an audio file');
      return;
    }
    
    setIsLoading(true);
    setError(null);
    
    try {
      const data = await uploadAudio(file);
      setIsLoading(false);
      setFile(null);
      onUploadSuccess(data);
    } catch (error) {
      setIsLoading(false);
      setError('Failed to process audio. Please try again.');
      console.error(error);
    }
  };

  return (
    <div className="upload-form">
      <h2>Upload Audio Recording</h2>
      <form onSubmit={handleSubmit}>
        <div className="file-input-container">
          <label className="file-input-label">
            {file ? file.name : 'Choose audio file'}
            <input
              type="file"
              accept="audio/*"
              onChange={handleFileChange}
              className="file-input"
            />
          </label>
        </div>
        
        <button 
          type="submit" 
          className="upload-button"
          disabled={isLoading || !file}
        >
          {isLoading ? 'Processing...' : 'Upload and Process'}
        </button>
        
        {error && <p className="error-message">{error}</p>}
      </form>
      
      <div className="supported-formats">
        <p>Supported formats: MP3, WAV, M4A</p>
        <p>Maximum file size: 50MB</p>
      </div>
    </div>
  );
};

export default UploadForm;