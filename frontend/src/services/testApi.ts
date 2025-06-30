import axios from 'axios';

export async function checkBackendHealth() {
  try {
    const response = await axios.get('/health');
    return response.data;
  } catch (error: any) {
    return { error: error.message };
  }
} 