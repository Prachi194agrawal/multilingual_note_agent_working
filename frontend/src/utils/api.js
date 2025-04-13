import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const uploadAudio = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await axios.post(`${API_URL}/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error uploading file:', error);
    throw error;
  }
};

export const getTranscriptions = async () => {
  try {
    const response = await axios.get(`${API_URL}/transcriptions`);
    return response.data;
  } catch (error) {
    console.error('Error fetching transcriptions:', error);
    throw error;
  }
};

export const getTranscription = async (id) => {
  try {
    const response = await axios.get(`${API_URL}/transcriptions/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching transcription ${id}:`, error);
    throw error;
  }
};

export const searchTranscriptions = async (query) => {
  try {
    const response = await axios.get(`${API_URL}/search?query=${query}`);
    return response.data;
  } catch (error) {
    console.error('Error searching transcriptions:', error);
    throw error;
  }
};

export const exportPDF = (id) => {
  window.open(`${API_URL}/export/${id}`, '_blank');
};