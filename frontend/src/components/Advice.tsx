import React, { useState, useEffect } from 'react';
import { apiService, AnalyticsSummary, Suggestions } from '../services/api';
import './Advice.css';

interface AdviceProps {
  refreshTrigger: number;
}

const Advice: React.FC<AdviceProps> = ({ refreshTrigger }) => {
  const [summary, setSummary] = useState<AnalyticsSummary | null>(null);
  const [aiInsights, setAiInsights] = useState<string>('');
  const [suggestions, setSuggestions] = useState<Suggestions | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchAnalytics = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await apiService.getAnalyticsSummary();
      setSummary(response.data);
      
      // Get AI insights
      const insightsResponse = await apiService.getAIInsights();
      setAiInsights(insightsResponse.data);
      
      // Get suggestions
      const suggestionsResponse = await apiService.getSuggestions();
      setSuggestions(suggestionsResponse.data);
    } catch (err: any) {
      console.error('Error fetching analytics:', err);
      
      // Provide more specific error messages
      if (err.response?.status === 401) {
        setError('Authentication required. Please log in again.');
      } else if (err.response?.status === 404) {
        setError('Analytics data not found. Please try adding some journal entries first.');
      } else if (err.response?.status >= 500) {
        setError('Server error. Please try again later.');
      } else if (err.code === 'NETWORK_ERROR' || err.message?.includes('Network Error')) {
        setError('Network error. Please check your connection and try again.');
      } else {
        setError('Failed to fetch analytics data. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAnalytics();
  }, [refreshTrigger]);

  if (loading) {
    return (
      <div className="advice-container">
        <div className="loading">Loading your personalized advice...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="advice-container">
        <div className="error">
          <h2>⚠️ Unable to Load Your Data</h2>
          <p>{error}</p>
          <p>This might be due to a connection issue or authentication problem.</p>
          <button 
            onClick={fetchAnalytics} 
            className="retry-button"
            style={{
              padding: '10px 20px',
              backgroundColor: '#667eea',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer',
              fontSize: '16px',
              marginTop: '15px'
            }}
          >
            🔄 Try Again
          </button>
          
          {/* Show suggestions even when there's an error */}
          {suggestions && (
            <div className="advice-section" style={{ marginTop: '30px' }}>
              <h2>💡 Wellness Suggestions</h2>
              <p className="suggestions-intro">While we resolve the technical issue, here are some wellness suggestions:</p>
              
              <div className="suggestions-grid">
                {suggestions.categories.slice(0, 4).map((category, categoryIndex) => (
                  <div key={categoryIndex} className="suggestion-category">
                    <h3>{category.title}</h3>
                    <ul className="suggestion-list">
                      {category.suggestions.slice(0, 3).map((suggestion, suggestionIndex) => (
                        <li key={suggestionIndex} className="suggestion-item">
                          {suggestion}
                        </li>
                      ))}
                    </ul>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    );
  }

  if (!summary || summary.total_entries < 5) {
    return (
      <div className="advice-container">
        <div className="insufficient-data">
          <h2>📊 Need More Data for Personalized Advice</h2>
          <p>You've tracked {summary?.total_entries || 0} mood entries so far. We need at least 5 entries to provide personalized insights.</p>
          <p>Keep journaling daily to unlock personalized advice and insights!</p>
          <div className="progress-bar">
            <div 
              className="progress-fill" 
              style={{ width: `${Math.min((summary?.total_entries || 0) / 5 * 100, 100)}%` }}
            ></div>
          </div>
          <p>{5 - (summary?.total_entries || 0)} more entries needed</p>
          
          {/* Show suggestions even when analytics data is insufficient */}
          {suggestions && (
            <div className="advice-section" style={{ marginTop: '30px' }}>
              <h2>💡 General Wellness Suggestions</h2>
              <p className="suggestions-intro">While we build your personalized insights, here are some general wellness suggestions:</p>
              
              <div className="suggestions-grid">
                {suggestions.categories.slice(0, 4).map((category, categoryIndex) => (
                  <div key={categoryIndex} className="suggestion-category">
                    <h3>{category.title}</h3>
                    <ul className="suggestion-list">
                      {category.suggestions.slice(0, 3).map((suggestion, suggestionIndex) => (
                        <li key={suggestionIndex} className="suggestion-item">
                          {suggestion}
                        </li>
                      ))}
                    </ul>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="advice-container">
      <h1>🧠 Personalized Mental Health Advice</h1>
      
      <div className="advice-section">
        <h2>💡 Your Personal Insights</h2>
        <div className="ai-insights">
          {aiInsights ? (
            <div className="insights-content">
              {aiInsights.split('\n\n').map((paragraph, index) => (
                <div key={index} className="insight-paragraph">
                  {paragraph.split('\n').map((line, lineIndex) => {
                    if (line.startsWith('•')) {
                      return (
                        <div key={lineIndex} className="insight-bullet">
                          {line}
                        </div>
                      );
                    } else if (line.startsWith('💡') || line.startsWith('🌟') || line.startsWith('💙') || 
                               line.startsWith('🔥') || line.startsWith('😰') || line.startsWith('😲') ||
                               line.startsWith('🤢') || line.startsWith('❤️') || line.startsWith('😐') ||
                               line.startsWith('✨') || line.startsWith('📊') || line.startsWith('🎯') ||
                               line.startsWith('📝') || line.startsWith('🤔') || line.startsWith('💝') ||
                               line.startsWith('🤗')) {
                      return (
                        <div key={lineIndex} className="insight-highlight">
                          {line}
                        </div>
                      );
                    } else if (line.trim()) {
                      return (
                        <p key={lineIndex} className="insight-text">
                          {line}
                        </p>
                      );
                    }
                    return null;
                  })}
                </div>
              ))}
            </div>
          ) : (
            <div className="loading-insights">Generating personalized insights...</div>
          )}
        </div>
      </div>

      <div className="advice-section">
        <h2>📈 Your Emotional Journey</h2>
        <div className="mood-summary">
          <div className="summary-card">
            <h3>Total Entries</h3>
            <p className="summary-number">{summary.total_entries}</p>
            <p className="summary-label">days of reflection</p>
          </div>
          <div className="summary-card">
            <h3>Most Common Emotion</h3>
            <p className="summary-emotion">{summary.most_common_emotion}</p>
            <p className="summary-label">your emotional baseline</p>
          </div>
          <div className="summary-card">
            <h3>Current Mood</h3>
            <p className="summary-emotion">{summary.recent_emotion}</p>
            <p className="summary-label">how you're feeling now</p>
          </div>
          <div className="summary-card">
            <h3>Emotional Clarity</h3>
            <p className="summary-number">{(summary.average_confidence * 100).toFixed(0)}%</p>
            <p className="summary-label">how clearly you express emotions</p>
          </div>
        </div>
      </div>

      <div className="advice-section">
        <h2>💪 Gentle Self-Care Suggestions</h2>
        <div className="self-care-tips">
          <div className="tip">
            <h3>🌅 Morning Grounding</h3>
            <p>Start with 5 minutes of deep breathing or gentle stretching to set a positive tone for your day.</p>
          </div>
          <div className="tip">
            <h3>📝 Continue Your Journey</h3>
            <p>Keep journaling regularly - you're building valuable self-awareness with every entry.</p>
          </div>
          <div className="tip">
            <h3>🏃‍♀️ Gentle Movement</h3>
            <p>Even a short walk or gentle stretching can help release tension and improve your mood.</p>
          </div>
          <div className="tip">
            <h3>😴 Restorative Sleep</h3>
            <p>Create a calming bedtime routine to support 7-9 hours of quality sleep.</p>
          </div>
          <div className="tip">
            <h3>🤝 Meaningful Connections</h3>
            <p>Reach out to someone you trust. Even a brief conversation can provide comfort and perspective.</p>
          </div>
          <div className="tip">
            <h3>🎯 Small Steps Forward</h3>
            <p>Break overwhelming tasks into tiny, manageable steps. Progress, not perfection.</p>
          </div>
        </div>
      </div>

      <div className="advice-section">
        <h2>🤗 When to Consider Professional Support</h2>
        <div className="warning-signs">
          <p>It's completely normal to need extra support sometimes. Consider reaching out to a mental health professional if you experience:</p>
          <ul>
            <li>Persistent feelings of sadness, anxiety, or hopelessness that don't seem to lift</li>
            <li>Difficulty with daily activities like work, relationships, or self-care</li>
            <li>Thoughts of self-harm or feeling like life isn't worth living</li>
            <li>Using substances to cope with difficult emotions</li>
            <li>Significant changes in sleep, appetite, or energy that last for weeks</li>
            <li>Withdrawing from activities or people you usually enjoy</li>
          </ul>
          <div className="support-message">
            <p><strong>Remember:</strong> Seeking help is a sign of strength and self-care. Mental health professionals are trained to help you navigate difficult emotions and develop healthy coping strategies. You don't have to face challenges alone.</p>
          </div>
        </div>
      </div>

      {suggestions && (
        <div className="advice-section">
          <h2>💡 Wellness Suggestions</h2>
          <p className="suggestions-intro">Here are some gentle suggestions to support your mental health and well-being. Choose what resonates with you:</p>
          
          <div className="suggestions-grid">
            {suggestions.categories.map((category, categoryIndex) => (
              <div key={categoryIndex} className="suggestion-category">
                <h3>{category.title}</h3>
                <ul className="suggestion-list">
                  {category.suggestions.map((suggestion, suggestionIndex) => (
                    <li key={suggestionIndex} className="suggestion-item">
                      {suggestion}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
          
          <div className="suggestions-footer">
            <p>💝 Remember: These are gentle suggestions, not prescriptions. Choose what feels right for you, and be kind to yourself in the process.</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default Advice; 