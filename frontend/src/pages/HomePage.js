import React, { useState, useEffect } from 'react';
import UploadForm from '../components/UploadForm';
import TranscriptionList from '../components/TranscriptionList';
import TranscriptionView from '../components/TranscriptionView';
import SearchBar from '../components/SearchBar';
import { getTranscriptions, getTranscription, searchTranscriptions } from '../utils/api';
import './HomePage.css';

const HomePage = () => {
  const [transcriptions, setTranscriptions] = useState([]);
  const [selectedTranscription, setSelectedTranscription] = useState(null);
  const [selectedId, setSelectedId] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchTranscriptions = async () => {
    try {
      setIsLoading(true);
      const data = await getTranscriptions();
      setTranscriptions(data);
      setIsLoading(false);
    } catch (error) {
      setError('Failed to load transcriptions');
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchTranscriptions();
  }, []);

  const handleTranscriptionSelect = async (id) => {
    try {
      setSelectedId(id);
      const data = await getTranscription(id);
      setSelectedTranscription(data);
    } catch (error) {
      setError('Failed to load transcription details');
    }
  };

  const handleSearch = async (query) => {
    if (!query.trim()) {
      fetchTranscriptions();
      return;
    }

    try {
      setIsLoading(true);
      const results = await searchTranscriptions(query);
      setTranscriptions(results);
      setIsLoading(false);

      if (results.length > 0 && (!selectedId || !results.some(t => t.id === selectedId))) {
        handleTranscriptionSelect(results[0].id);
      }
    } catch (error) {
      setError('Search failed');
      setIsLoading(false);
    }
  };

  const handleUploadSuccess = async (data) => {
    await fetchTranscriptions();
    handleTranscriptionSelect(data.id);
  };

  return (
    <div className="home-page">
      <header className="app-header">
        <h1>Multilingual Meeting Notes</h1>
        <SearchBar onSearch={handleSearch} />
      </header>

      <div className="main-content">
        <div className="sidebar">
          <UploadForm onUploadSuccess={handleUploadSuccess} />
          {isLoading ? (
            <p className="loading">Loading transcriptions...</p>
          ) : (
            <TranscriptionList
              transcriptions={transcriptions}
              onSelect={handleTranscriptionSelect}
              selectedId={selectedId}
            />
          )}
        </div>

        <div className="content-area">
          {error && <p className="error-message">{error}</p>}
          {selectedTranscription ? (
            <TranscriptionView transcription={selectedTranscription} />
          ) : (
            <div className="empty-state">
              <h2>Welcome to Multilingual Meeting Notes</h2>
              <p>Upload an audio recording or select an existing transcription to get started.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default HomePage;