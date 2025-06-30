import React, { useState, useEffect } from 'react';
import { apiService, JournalEntry, Suggestions, AnalyticsSummary } from '../services/api';
import './Advice.css';

const SELF_CARE_SUGGESTIONS = [
  {
    emoji: '🌅',
    title: 'Morning Grounding',
    desc: 'Start with 5 minutes of deep breathing or gentle stretching to set a positive tone for your day.'
  },
  {
    emoji: '📝',
    title: 'Continue Your Journey',
    desc: `Keep journaling regularly - you're building valuable self-awareness with every entry.`
  },
  {
    emoji: '🏃‍♂️',
    title: 'Gentle Movement',
    desc: 'Even a short walk or gentle stretching can help release tension and improve your mood.'
  },
  {
    emoji: '😴',
    title: 'Restorative Sleep',
    desc: 'Create a calming bedtime routine to support 7-9 hours of quality sleep.'
  },
  {
    emoji: '🤝',
    title: 'Meaningful Connections',
    desc: 'Reach out to someone you trust. Even a brief conversation can provide comfort and perspective.'
  },
  {
    emoji: '🎯',
    title: 'Small Steps Forward',
    desc: 'Break overwhelming tasks into tiny, manageable steps. Progress, not perfection.'
  }
];

const PROFESSIONAL_SUPPORT_SIGNS = [
  "Persistent feelings of sadness, anxiety, or hopelessness that don't seem to lift",
  'Difficulty with daily activities like work, relationships, or self-care',
  "Thoughts of self-harm or feeling like life isn't worth living",
  'Using substances to cope with difficult emotions',
  'Significant changes in sleep, appetite, or energy that last for weeks',
  'Withdrawing from activities or people you usually enjoy',
];

const Advice: React.FC = () => {
  const [entries, setEntries] = useState<JournalEntry[]>([]);
  const [insights, setInsights] = useState<any>(null);
  const [suggestions, setSuggestions] = useState<Suggestions | null>(null);
  const [loading, setLoading] = useState(true);
  const [insightsLoading, setInsightsLoading] = useState(true);
  const [error, setError] = useState('');
  const [insightsError, setInsightsError] = useState('');
  const [analytics, setAnalytics] = useState<AnalyticsSummary | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError('');
      try {
        const entriesRes = await apiService.getJournalEntries();
        setEntries(Array.isArray(entriesRes.entries) ? entriesRes.entries : []);
        const suggestionsRes = await apiService.getSuggestions();
        setSuggestions(suggestionsRes);
        const analyticsRes = await apiService.getAnalyticsSummary();
        setAnalytics(analyticsRes);
      } catch (err: any) {
        setError('Failed to load advice data.');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  useEffect(() => {
    if (Array.isArray(entries) && entries.length >= 5) {
      setInsightsLoading(true);
      setInsightsError('');
      apiService.getAIInsights()
        .then((res) => {
          setInsights(res.insights || res);
        })
        .catch(() => {
          setInsightsError('Failed to load AI insights.');
        })
        .finally(() => setInsightsLoading(false));
    }
  }, [entries]);

  if (loading) {
    return <div className="advice-container"><div className="loading">Loading advice...</div></div>;
  }

  if (error && (!Array.isArray(entries) || entries.length === 0)) {
    return <div className="advice-container"><div className="error">{error}</div></div>;
  }

  if (!Array.isArray(entries) || entries.length < 5) {
    return (
      <div className="advice-container">
        <div className="insufficient-data">
          <h2>📊 Need More Data for Personalized Advice</h2>
          <p>You've tracked {Array.isArray(entries) ? entries.length : 0} mood entries so far. We need at least 5 entries to provide personalized insights.</p>
          <p>Keep journaling daily to unlock personalized advice and insights!</p>
          <div className="progress-bar">
            <div className="progress-fill" style={{ width: `${Math.min((Array.isArray(entries) ? entries.length : 0) / 5 * 100, 100)}%` }}></div>
          </div>
          <p>{5 - (Array.isArray(entries) ? entries.length : 0)} more entries needed</p>
        </div>
        {Array.isArray(entries) && entries.length > 0 && (
          <div className="recent-entries">
            <h3 style={{ marginTop: 32, marginBottom: 12 }}>Your Recent Entries</h3>
            <ul style={{ listStyle: 'none', padding: 0 }}>
              {entries.slice(-5).reverse().map((entry, idx) => (
                <li key={entry.id || idx} style={{ background: '#f8f9fa', borderRadius: 8, marginBottom: 12, padding: 16, boxShadow: '0 2px 8px rgba(0,0,0,0.04)' }}>
                  <div style={{ fontWeight: 600, fontSize: 16, marginBottom: 4 }}>{entry.text}</div>
                  <div style={{ color: '#888', fontSize: 14 }}>Mood: <b>{entry.dominant_emotion || '-'}</b> | {new Date(entry.timestamp).toLocaleString()}</div>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="advice-container">
      {/* Section 1: Personal Insights */}
      <div className="advice-section">
        <h2 style={{ fontWeight: 800, fontSize: '2rem', marginBottom: 10 }}>💡 Your Personal Insights</h2>
        {insightsLoading ? (
          <div className="loading-insights">Loading AI insights...</div>
        ) : insightsError ? (
          <div className="error">{insightsError}</div>
        ) : insights ? (
          <div className="ai-insights">
            {/* Warm Introduction */}
            {insights.intro && (
              <div className="gradient-intro" style={{
                borderRadius: 16,
                padding: '24px 28px',
                marginBottom: 24,
                color: 'white',
                fontSize: 18,
                fontWeight: 600,
                lineHeight: 1.6,
                boxShadow: '0 8px 24px rgba(102, 126, 234, 0.15)'
              }}>
                {insights.intro}
              </div>
            )}

            {/* Detailed Insights */}
            {insights.insights && Array.isArray(insights.insights) && insights.insights.length > 0 && (
              <div style={{ marginBottom: 32 }}>
                <div className="insights-section-header">
                  <h3 style={{ 
                    color: '#2c3e50', 
                    fontWeight: 700, 
                    fontSize: 22, 
                    marginBottom: 0
                  }}>
                    🔍 Detailed Analysis
                  </h3>
                </div>
                {insights.insights.map((insight: string, idx: number) => (
                  <div key={idx} className="insight-paragraph" style={{
                    background: 'linear-gradient(90deg, #f8fafc 0%, #e9ecef 100%)',
                    borderRadius: 12,
                    padding: '20px 24px',
                    marginBottom: 16,
                    borderLeft: '5px solid #667eea',
                    fontSize: 16,
                    fontWeight: 500,
                    color: '#2c3e50',
                    boxShadow: '0 4px 12px rgba(102, 126, 234, 0.07)',
                    lineHeight: 1.6
                  }}>
                    <span style={{ fontWeight: 600, color: '#667eea', marginRight: 8 }}>
                      {idx + 1}.
                    </span>
                    {insight}
                  </div>
                ))}
              </div>
            )}

            {/* Personalized Recommendations */}
            {insights.recommendations && Array.isArray(insights.recommendations) && insights.recommendations.length > 0 && (
              <div style={{ marginBottom: 32 }}>
                <div className="insights-section-header">
                  <h3 style={{ 
                    color: '#2c3e50', 
                    fontWeight: 700, 
                    fontSize: 22, 
                    marginBottom: 0
                  }}>
                    🌱 Personalized Recommendations
                  </h3>
                </div>
                <div className="recommendation-card" style={{
                  background: 'linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 100%)',
                  borderRadius: 16,
                  padding: '24px 28px',
                  border: '2px solid #e1f5fe'
                }}>
                  {insights.recommendations.map((rec: string, idx: number) => (
                    <div key={idx} className="recommendation-item" style={{
                      display: 'flex',
                      alignItems: 'flex-start',
                      marginBottom: 12,
                      padding: '12px 16px',
                      background: 'white',
                      borderRadius: 8,
                      boxShadow: '0 2px 8px rgba(0,0,0,0.05)'
                    }}>
                      <span className="recommendation-number" style={{
                        background: '#667eea',
                        color: 'white',
                        borderRadius: '50%',
                        width: 24,
                        height: 24,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontSize: 12,
                        fontWeight: 700,
                        marginRight: 12,
                        flexShrink: 0
                      }}>
                        {idx + 1}
                      </span>
                      <span style={{ fontSize: 16, lineHeight: 1.5, color: '#2c3e50' }}>
                        {rec}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Emotional Journey Summary */}
            {insights.emotional_journey && insights.emotional_journey.summary && (
              <div className="emotional-journey-summary" style={{
                background: 'linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%)',
                borderRadius: 16,
                padding: '24px 28px',
                border: '2px solid #ffcc02',
                marginBottom: 24
              }}>
                <h3 style={{ 
                  color: '#e65100', 
                  fontWeight: 700, 
                  fontSize: 20, 
                  marginBottom: 12,
                  display: 'flex',
                  alignItems: 'center',
                  gap: 8
                }}>
                  🧭 Your Emotional Journey Summary
                </h3>
                <p style={{ 
                  fontSize: 17, 
                  lineHeight: 1.6, 
                  color: '#bf360c',
                  fontWeight: 500,
                  margin: 0
                }}>
                  {insights.emotional_journey.summary}
                </p>
              </div>
            )}
          </div>
        ) : (
          <div className="loading-insights">No insights available yet. Add more journal entries to get personalized insights!</div>
        )}
      </div>

      {/* Section 2: Your Emotional Journey (summary/intro + stats) */}
      <div className="advice-section" style={{ background: 'linear-gradient(90deg, #f8fafc 0%, #e9ecef 100%)', borderLeft: '5px solid #667eea', marginBottom: 32 }}>
        <h2 style={{ fontWeight: 800, fontSize: '2rem', marginBottom: 10 }}>🧭 Your Emotional Journey</h2>
        
        {/* Use AI insights summary if available, otherwise use analytics */}
        {insights && insights.emotional_journey && insights.emotional_journey.summary && !insightsLoading && !insightsError ? (
          <div style={{ fontWeight: 600, fontSize: 18, marginBottom: 24, color: '#2c3e50', lineHeight: 1.6 }}>
            {insights.emotional_journey.summary}
          </div>
        ) : insights && insights.intro && !insightsLoading && !insightsError ? (
          <div style={{ fontWeight: 600, fontSize: 18, marginBottom: 24, color: '#2c3e50', lineHeight: 1.6 }}>
            {insights.intro}
          </div>
        ) : null}

        {/* Stats Cards - Use AI insights data if available, otherwise fallback to analytics */}
        <div style={{ display: 'flex', gap: 24, flexWrap: 'wrap', marginTop: 8 }}>
          <div className="stats-card" style={{ background: '#fff', borderRadius: 16, boxShadow: '0 2px 8px rgba(102,126,234,0.07)', padding: 24, minWidth: 220, textAlign: 'center', flex: 1 }}>
            <div style={{ fontWeight: 700, fontSize: 20, marginBottom: 4 }}>Total Entries</div>
            <div style={{ color: '#667eea', fontWeight: 800, fontSize: 32, marginBottom: 2 }}>
              {insights?.emotional_journey?.stats?.total_entries || analytics?.total_entries || 0}
            </div>
            <div style={{ color: '#888', fontStyle: 'italic', fontSize: 15 }}>days of reflection</div>
          </div>
          <div className="stats-card" style={{ background: '#fff', borderRadius: 16, boxShadow: '0 2px 8px rgba(102,126,234,0.07)', padding: 24, minWidth: 220, textAlign: 'center', flex: 1 }}>
            <div style={{ fontWeight: 700, fontSize: 20, marginBottom: 4 }}>Most Common Emotion</div>
            <div style={{ color: '#667eea', fontWeight: 800, fontSize: 32, marginBottom: 2, textShadow: '0 2px 6px #e9ecef' }}>
              {(insights?.emotional_journey?.stats?.most_common_emotion || analytics?.most_common_emotion || '-').charAt(0).toUpperCase() + 
               (insights?.emotional_journey?.stats?.most_common_emotion || analytics?.most_common_emotion || '-').slice(1)}
            </div>
            <div style={{ color: '#888', fontStyle: 'italic', fontSize: 15 }}>your emotional baseline</div>
          </div>
          <div className="stats-card" style={{ background: '#fff', borderRadius: 16, boxShadow: '0 2px 8px rgba(102,126,234,0.07)', padding: 24, minWidth: 220, textAlign: 'center', flex: 1 }}>
            <div style={{ fontWeight: 700, fontSize: 20, marginBottom: 4 }}>Current Mood</div>
            <div style={{ color: '#667eea', fontWeight: 800, fontSize: 32, marginBottom: 2 }}>
              {(insights?.emotional_journey?.stats?.current_mood || analytics?.current_mood || '-').charAt(0).toUpperCase() + 
               (insights?.emotional_journey?.stats?.current_mood || analytics?.current_mood || '-').slice(1)}
            </div>
            <div style={{ color: '#888', fontStyle: 'italic', fontSize: 15 }}>how you're feeling now</div>
          </div>
          <div className="stats-card" style={{ background: '#fff', borderRadius: 16, boxShadow: '0 2px 8px rgba(102,126,234,0.07)', padding: 24, minWidth: 220, textAlign: 'center', flex: 1 }}>
            <div style={{ fontWeight: 700, fontSize: 20, marginBottom: 4 }}>Emotional Clarity</div>
            <div style={{ color: '#667eea', fontWeight: 800, fontSize: 32, marginBottom: 2 }}>
              {insights?.emotional_journey?.stats?.emotional_clarity || 
               (analytics?.average_confidence ? Math.round(analytics.average_confidence * 100) + '%' : '-')}
            </div>
            <div style={{ color: '#888', fontStyle: 'italic', fontSize: 15 }}>how clearly you express emotions</div>
          </div>
        </div>
      </div>

      {/* Section 3: Gentle Self-Care Suggestions */}
      <div className="advice-section">
        <h2 style={{ fontWeight: 800, fontSize: '2rem', marginBottom: 10 }}>💪 Gentle Self-Care Suggestions</h2>
        <hr style={{ margin: '16px 0 24px 0', border: 'none', borderTop: '2px solid #ececec' }} />
        <div className="resources-grid">
          {SELF_CARE_SUGGESTIONS.map((tip, idx) => (
            <div className="resource-card" key={idx}>
              <h3 style={{ fontWeight: 700, fontSize: '1.2rem', marginBottom: 8 }}>
                <span style={{ marginRight: 8 }}>{tip.emoji}</span>{tip.title}
              </h3>
              <p style={{ color: '#555', fontSize: '1.05rem', margin: 0 }}>{tip.desc}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Section 4: When to Consider Professional Support */}
      <div className="advice-section">
        <h2 style={{ fontWeight: 800, fontSize: '2rem', marginBottom: 10 }}>🤗 When to Consider Professional Support</h2>
        <hr style={{ margin: '16px 0 24px 0', border: 'none', borderTop: '2px solid #ececec' }} />
        <div style={{ background: '#ffeaea', borderRadius: 16, padding: 24, borderLeft: '6px solid #e57373', marginBottom: 18 }}>
          <div style={{ fontSize: '1.15rem', marginBottom: 12 }}>
            It's completely normal to need extra support sometimes. Consider reaching out to a mental health professional if you experience:
          </div>
          <ul style={{ fontSize: '1.08rem', color: '#b23b3b', marginLeft: 18, marginBottom: 0 }}>
            {PROFESSIONAL_SUPPORT_SIGNS.map((sign, idx) => (
              <li key={idx} style={{ marginBottom: 8 }}>{sign}</li>
            ))}
          </ul>
        </div>
        <div style={{ background: 'linear-gradient(90deg, #667eea 0%, #8ec5fc 100%)', borderRadius: 12, padding: 18, color: 'white', fontWeight: 600, fontSize: '1.1rem', boxShadow: '0 2px 8px rgba(102, 126, 234, 0.10)' }}>
          <span style={{ fontWeight: 700 }}>Remember:</span> Seeking help is a sign of strength and self-care. Mental health professionals are trained to help you navigate difficult emotions and develop healthy coping strategies. You don't have to face challenges alone.
        </div>
      </div>

      {/* Section 5: Wellness Suggestions (from backend or fallback) */}
      <div className="advice-section">
        <h2 style={{ fontWeight: 800, fontSize: '2rem', marginBottom: 10 }}>💡 Wellness Suggestions</h2>
        <div className="suggestions-grid">
          {suggestions && Array.isArray(suggestions.categories)
            ? suggestions.categories.map((category, categoryIndex) => (
                <div key={categoryIndex} className="suggestion-category">
                  <h3>{category.title}</h3>
                  <ul className="suggestion-list">
                    {category.suggestions.map((suggestion, suggestionIndex) => (
                      <li key={suggestionIndex} className="suggestion-item">{suggestion}</li>
                    ))}
                  </ul>
                </div>
              ))
            : <div style={{ color: '#888', fontStyle: 'italic' }}>No wellness suggestions available at the moment.</div>
          }
        </div>
        {/* Gentle Reminder Bar */}
        <div className="gentle-reminder-bar">
          <span role="img" aria-label="reminder" style={{ fontSize: 26, marginRight: 10 }}>💖</span>
          <span>Remember: These are gentle suggestions, not prescriptions. Choose what feels right for you, and be kind to yourself in the process.</span>
        </div>
      </div>
    </div>
  );
};

export default Advice; 