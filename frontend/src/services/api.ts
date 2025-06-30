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
  emotion?: string;
  confidence: number;
  timestamp: string;
  date: string;
  sentiment_score?: number;
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

// Helper function to extract data from backend response
const extractData = (response: any) => {
  if (response.data && response.data.success !== undefined) {
    // Backend wraps data in { success: true, data: ... } or { success: true, summary: ... }
    return response.data.summary || response.data.entries || response.data.timeline || response.data.analysis || response.data;
  }
  return response.data;
};

export const apiService = {
  // Health check
  health: () => api.get('/health'),

  // Journal entries
  addJournalEntry: (text: string) =>
    api.post('/journal', { text }).then(extractData),

  getJournalEntries: () =>
    api.get<{success: boolean, entries: JournalEntry[], count: number}>('/journal').then(response => {
      // Return the response directly so we can access both entries and count
      return response.data;
    }),

  // Analytics
  getAnalyticsSummary: () =>
    api.get<AnalyticsSummary>('/analytics/summary').then(extractData),

  getTimeline: (limit: number = 30) =>
    api.get<TimelineEntry[]>(`/analytics/timeline?limit=${limit}`).then(extractData),

  // AI Insights
  getAIInsights: () =>
    api.get('/ai/insights').then(extractData),

  // Suggestions
  getSuggestions: () =>
    api.get('/suggestions').then(res => res.data.suggestions),

  // Text analysis
  analyzeText: (text: string) =>
    api.post<any>('/analyze', { text }).then(extractData),

  // Authentication
  getCurrentUser: () => api.get('/auth/user'),
  demoLogin: () => api.get('/auth/demo'),
};

export default apiService; 