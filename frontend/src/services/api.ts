import axios from 'axios';

const API_BASE_URL = 'http://localhost:5001';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface JournalEntry {
  id: number;
  user_id: string;
  text: string;
  emotion: string;
  confidence: number;
  timestamp: string;
  analysis: any;
}

export interface AnalyticsSummary {
  total_entries: number;
  emotion_distribution: Record<string, number>;
  average_confidence: number;
  most_common_emotion: string;
  recent_emotion: string;
}

export interface TimelineEntry {
  id: number;
  date: string;
  emotion: string;
  confidence: number;
  text: string;
}

export interface AIInsights {
  insights: string;
}

export const apiService = {
  // Health check
  health: () => api.get('/health'),

  // Journal entries
  addJournalEntry: (text: string, user_id: string = 'user123') =>
    api.post<JournalEntry>('/journal', { text, user_id }),

  getJournalEntries: (limit: number = 10, user_id: string = 'user123') =>
    api.get<JournalEntry[]>(`/journal?limit=${limit}&user_id=${user_id}`),

  // Analytics
  getAnalyticsSummary: (user_id: string = 'user123') =>
    api.get<AnalyticsSummary>(`/analytics/summary?user_id=${user_id}`),

  getTimeline: (user_id: string = 'user123', limit: number = 20) =>
    api.get<{ timeline: TimelineEntry[]; count: number }>(`/analytics/timeline?user_id=${user_id}&limit=${limit}`),

  // AI Insights
  getAIInsights: (data: AnalyticsSummary) =>
    api.post<AIInsights>('/ai/insights', data),

  // Text analysis
  analyzeText: (text: string) =>
    api.post<any>('/analyze', { text }),
};

export default apiService; 