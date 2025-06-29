import axios from 'axios';

const API_BASE_URL = 'http://localhost:5001';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Include cookies for authentication
});

export interface JournalEntry {
  id: number;
  text: string;
  dominant_emotion: string;
  confidence: number;
  timestamp: string;
  analysis?: any;
}

export interface AnalyticsSummary {
  total_entries: number;
  emotion_distribution: Record<string, number>;
  average_confidence: number;
  most_common_emotion: string;
  recent_emotion: string;
  current_mood: string;
}

export interface TimelineEntry {
  id: number;
  text: string;
  dominant_emotion: string;
  confidence: number;
  timestamp: string;
  date: string;
}

export interface AIInsights {
  insights: string;
}

export interface SuggestionCategory {
  title: string;
  suggestions: string[];
}

export interface Suggestions {
  categories: SuggestionCategory[];
}

export const apiService = {
  // Health check
  health: () => api.get('/health'),

  // Journal entries
  addJournalEntry: (text: string) =>
    api.post<JournalEntry>('/journal', { text }),

  getJournalEntries: (limit: number = 10) =>
    api.get<JournalEntry[]>(`/journal?limit=${limit}`),

  clearJournalEntries: () =>
    api.delete<{message: string, deleted_count: number}>('/journal/clear'),

  // Analytics
  getAnalyticsSummary: () =>
    api.get<AnalyticsSummary>('/analytics/summary'),

  getTimeline: (limit: number = 30) =>
    api.get<TimelineEntry[]>(`/analytics/timeline?limit=${limit}`),

  // AI Insights
  getAIInsights: () =>
    api.post<string>('/ai/insights', {}),

  // Suggestions
  getSuggestions: () =>
    api.get<Suggestions>('/suggestions'),

  // Text analysis
  analyzeText: (text: string) =>
    api.post<any>('/analyze', { text }),

  // Authentication
  getCurrentUser: () => api.get('/auth/user'),
  demoLogin: () => api.get('/auth/demo'),
};

export default apiService; 