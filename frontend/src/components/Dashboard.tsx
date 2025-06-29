import React, { useState, useEffect, useCallback } from 'react';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Link } from 'react-router-dom';
import { apiService, AnalyticsSummary, JournalEntry } from '../services/api';
import './Dashboard.css';

interface Quote {
  text: string;
  author: string;
}

const Dashboard: React.FC<{ refreshTrigger: number }> = ({ refreshTrigger }) => {
  const [summary, setSummary] = useState<AnalyticsSummary | null>(null);
  const [currentMood, setCurrentMood] = useState<JournalEntry | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [quote, setQuote] = useState<Quote | null>(null);
  const [quoteLoading, setQuoteLoading] = useState(true);

  const fetchDailyQuote = useCallback(async () => {
    try {
      // Try multiple quote APIs for better reliability
      const apis = [
        'https://api.quotable.io/random',
        'https://zenquotes.io/api/random',
        'https://api.goprogram.ai/inspiration'
      ];

      for (const api of apis) {
        try {
          const response = await fetch(api);
          if (response.ok) {
            const data = await response.json();
            
            if (api.includes('quotable.io')) {
              setQuote({
                text: data.content,
                author: data.author
              });
              break;
            } else if (api.includes('zenquotes.io')) {
              setQuote({
                text: data[0].q,
                author: data[0].a
              });
              break;
            } else if (api.includes('goprogram.ai')) {
              setQuote({
                text: data.quote,
                author: data.author
              });
              break;
            }
          }
        } catch (err) {
          console.log(`Failed to fetch from ${api}, trying next...`);
          continue;
        }
      }

      // Fallback to a motivational quote if all APIs fail
      if (!quote) {
        const fallbackQuotes = [
          { text: "The only way to do great work is to love what you do.", author: "Steve Jobs" },
          { text: "Life is 10% what happens to you and 90% how you react to it.", author: "Charles R. Swindoll" },
          { text: "The greatest glory in living lies not in never falling, but in rising every time we fall.", author: "Nelson Mandela" },
          { text: "Your emotions are the slaves to your thoughts, and you are the slave to your emotions.", author: "Elizabeth Gilbert" },
          { text: "Happiness is not something ready made. It comes from your own actions.", author: "Dalai Lama" }
        ];
        const randomQuote = fallbackQuotes[Math.floor(Math.random() * fallbackQuotes.length)];
        setQuote(randomQuote);
      }
    } catch (err) {
      console.error('Error fetching quote:', err);
      // Set a default quote if everything fails
      setQuote({
        text: "Every day is a new beginning. Take a deep breath and start again.",
        author: "Anonymous"
      });
    } finally {
      setQuoteLoading(false);
    }
  }, [quote]);

  const fetchAnalytics = useCallback(async () => {
    setLoading(true);
    setError('');
    
    try {
      const response = await apiService.getAnalyticsSummary();
      setSummary(response.data);
      
      // Get current mood (most recent entry)
      const journalResponse = await apiService.getJournalEntries(1);
      if (journalResponse.data && journalResponse.data.length > 0) {
        setCurrentMood(journalResponse.data[0]);
      }
    } catch (err) {
      // Don't show error for empty data, just set summary to null
      console.log('No analytics data available yet');
      setSummary(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchAnalytics();
    fetchDailyQuote();
  }, [refreshTrigger, fetchAnalytics, fetchDailyQuote]);

  const getEmotionColor = (emotion: string): string => {
    const colors: Record<string, string> = {
      joy: '#FFD700',
      sadness: '#4682B4',
      anger: '#DC143C',
      fear: '#8B4513',
      surprise: '#FF69B4',
      disgust: '#228B22',
      love: '#FF1493',
      neutral: '#808080'
    };
    return colors[emotion] || '#8884d8';
  };

  if (loading) {
    return (
      <div className="dashboard-container">
        <div className="loading">Loading your mood insights...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard-container">
        <div className="error">{error}</div>
      </div>
    );
  }

  if (!summary) {
    return (
      <div className="dashboard-container">
        <div className="no-data">
          <div className="no-data-content">
            <h2>📝 Start Your Mood Journey!</h2>
            <p>Add your first journal entry to see your emotional insights and patterns.</p>
            <div className="no-data-features">
              <div className="feature">
                <span>📊</span>
                <p>Track your emotions</p>
              </div>
              <div className="feature">
                <span>📈</span>
                <p>View mood trends</p>
              </div>
              <div className="feature">
                <span>🧠</span>
                <p>Get AI insights</p>
              </div>
            </div>
            <p className="no-data-cta">Head to the Journal page to get started!</p>
          </div>
        </div>
      </div>
    );
  }

  // Prepare data for charts
  const pieData = Object.entries(summary.emotion_distribution).map(([emotion, count]) => ({
    name: emotion,
    value: count,
    color: getEmotionColor(emotion)
  }));

  const barData = Object.entries(summary.emotion_distribution).map(([emotion, count]) => ({
    emotion,
    count,
    color: getEmotionColor(emotion)
  }));

  return (
    <div className="dashboard-container">
      {/* Quote Section */}
      <div className="dashboard-quote">
        {quoteLoading ? (
          <div className="quote-loading">Loading daily inspiration...</div>
        ) : quote ? (
          <blockquote>
            "{quote.text}"
            <footer>— {quote.author}</footer>
          </blockquote>
        ) : (
          <blockquote>
            "Every day is a new beginning. Take a deep breath and start again."
            <footer>— Anonymous</footer>
          </blockquote>
        )}
      </div>

      {/* Advice Notification */}
      {summary.total_entries >= 5 && (
        <div className="advice-notification">
          <div className="notification-content">
            <h3>🎉 You've unlocked personalized advice!</h3>
            <p>You've tracked {summary.total_entries} mood entries. Visit the Advice page for AI-powered insights and professional mental health resources.</p>
            <Link to="/advice" className="advice-link">Get Personalized Advice</Link>
          </div>
        </div>
      )}

      {/* Current Mood Display */}
      {currentMood && (
        <div className="current-mood">
          <h2>Current Mood</h2>
          <div className="mood-card">
            <div className="mood-emoji">
              {currentMood.dominant_emotion === 'joy' && '😊'}
              {currentMood.dominant_emotion === 'sadness' && '😢'}
              {currentMood.dominant_emotion === 'anger' && '😠'}
              {currentMood.dominant_emotion === 'fear' && '😨'}
              {currentMood.dominant_emotion === 'surprise' && '😲'}
              {currentMood.dominant_emotion === 'disgust' && '🤢'}
              {currentMood.dominant_emotion === 'love' && '❤️'}
              {currentMood.dominant_emotion === 'neutral' && '😐'}
            </div>
            <div className="mood-details">
              <h3>{currentMood.dominant_emotion.charAt(0).toUpperCase() + currentMood.dominant_emotion.slice(1)}</h3>
              <p className="confidence">Confidence: {(currentMood.confidence * 100).toFixed(1)}%</p>
              <p className="mood-text">"{currentMood.text}"</p>
            </div>
          </div>
        </div>
      )}

      {/* Summary Stats */}
      <div className="summary-stats">
        <div className="stat-card">
          <h3>Total Entries</h3>
          <p>{summary.total_entries}</p>
        </div>
        <div className="stat-card">
          <h3>Most Common</h3>
          <p>{summary.most_common_emotion}</p>
        </div>
        <div className="stat-card">
          <h3>Average Confidence</h3>
          <p>{(summary.average_confidence * 100).toFixed(1)}%</p>
        </div>
      </div>

      {/* Charts */}
      <div className="charts-container">
        <div className="chart-section">
          <h2>Emotion Distribution</h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${percent ? (percent * 100).toFixed(0) : 0}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {pieData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-section">
          <h2>Emotion Counts</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={barData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="emotion" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count">
                {barData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 