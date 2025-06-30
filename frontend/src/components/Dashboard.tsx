import React, { useState, useEffect, useCallback } from 'react';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Link } from 'react-router-dom';
import { apiService, AnalyticsSummary, JournalEntry } from '../services/api';
import './Dashboard.css';

interface Quote {
  text: string;
  author: string;
}

const Dashboard: React.FC = () => {
  const [summary, setSummary] = useState<AnalyticsSummary | null>(null);
  const [currentMood, setCurrentMood] = useState<JournalEntry | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [quote, setQuote] = useState<Quote | null>(null);
  const [quoteLoading, setQuoteLoading] = useState(true);

  // Map emotions to quote tags
  const moodToTag: Record<string, string[]> = {
    joy: ['happiness', 'inspiration', 'positive'],
    sadness: ['hope', 'perseverance', 'overcome'],
    anger: ['calm', 'forgiveness', 'peace'],
    fear: ['courage', 'confidence', 'bravery'],
    love: ['love', 'kindness', 'compassion'],
    surprise: ['life', 'wisdom', 'change'],
    neutral: ['life', 'wisdom', 'balance']
  };

  // Fetch a quote based on mood
  const fetchMoodQuote = useCallback(async (mood: string) => {
    setQuoteLoading(true);
    try {
      const tags = moodToTag[mood] || ['inspiration'];
      // Try Quotable API with tag
      const response = await fetch(`https://api.quotable.io/random?tags=${tags.join(',')}`);
      if (response.ok) {
        const data = await response.json();
        setQuote({ text: data.content, author: data.author });
        return;
      }
    } catch (err) {
      // Ignore and fallback
    }
    // Fallback quote
    setQuote({
      text: "Every day is a new beginning. Take a deep breath and start again.",
      author: "Anonymous"
    });
    setQuoteLoading(false);
  }, []);

  const fetchAnalytics = useCallback(async () => {
    setLoading(true);
    setError('');
    
    try {
      const summaryData = await apiService.getAnalyticsSummary();
      setSummary(summaryData);
      
      // Get current mood (most recent entry)
      const journalData = await apiService.getJournalEntries();
      if (journalData && journalData.entries && journalData.entries.length > 0) {
        setCurrentMood(journalData.entries[journalData.entries.length - 1]);
      }
    } catch (err) {
      // Don't show error for empty data, just set summary to null
      console.log('No analytics data available yet');
      setSummary(null);
    } finally {
      setLoading(false);
    }
  }, []);

  // Fetch analytics and quote
  useEffect(() => {
    fetchAnalytics();
  }, [fetchAnalytics]);

  // Fetch quote when current mood changes
  useEffect(() => {
    if (currentMood && currentMood.dominant_emotion) {
      fetchMoodQuote(currentMood.dominant_emotion);
    }
  }, [currentMood, fetchMoodQuote]);

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

  // Custom label renderer for pie chart (outside the pie)
  const renderCustomPieLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent, name, value }: any) => {
    if (!value) return null;
    const RADIAN = Math.PI / 180;
    const radius = outerRadius + 24;
    const x = cx + radius * Math.cos(-midAngle * RADIAN);
    const y = cy + radius * Math.sin(-midAngle * RADIAN);
    return (
      <text x={x} y={y} fill="#333" textAnchor={x > cx ? 'start' : 'end'} dominantBaseline="central" fontSize={14} fontWeight={500}>
        {`${name.charAt(0).toUpperCase() + name.slice(1)} (${(percent * 100).toFixed(0)}%)`}
      </text>
    );
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

  // Calculate total for legend
  const total = pieData.reduce((sum, entry) => sum + entry.value, 0);

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
              {currentMood.dominant_emotion === 'joy' && '😄'}
              {currentMood.dominant_emotion === 'sadness' && '😢'}
              {currentMood.dominant_emotion === 'anger' && '😠'}
              {currentMood.dominant_emotion === 'fear' && '😨'}
              {currentMood.dominant_emotion === 'surprise' && '😲'}
              {currentMood.dominant_emotion === 'disgust' && '🤢'}
              {currentMood.dominant_emotion === 'love' && '❤️'}
              {currentMood.dominant_emotion === 'neutral' && '🙂'}
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
          <div className="dashboard-stat">
            <div className="dashboard-stat-value">{summary.average_confidence.toFixed(1)}%</div>
          </div>
        </div>
      </div>

      {/* Charts */}
      <div className="charts-landscape-row" style={{ display: 'flex', flexDirection: 'row', gap: 32, flexWrap: 'wrap', justifyContent: 'center' }}>
        <div className="emotion-distribution-section" style={{ flex: 1, minWidth: 320, maxWidth: 400 }}>
          <h2>Emotion Distribution</h2>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie
                data={pieData}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={80}
                fill="#8884d8"
                label={renderCustomPieLabel}
              >
                {pieData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip formatter={(value: any, name: any) => [`${value}`, `${name}`]} />
            </PieChart>
          </ResponsiveContainer>
        </div>
        <div className="emotion-counts-section" style={{ flex: 1, minWidth: 320, maxWidth: 500 }}>
          <h2>Emotion Counts</h2>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={barData} margin={{ top: 16, right: 16, left: 0, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="emotion" tick={{ fontSize: 13 }} />
              <YAxis allowDecimals={false} tick={{ fontSize: 13 }} />
              <Tooltip />
              <Bar dataKey="count">
                {barData.map((entry, index) => (
                  <Cell key={`bar-cell-${index}`} fill={entry.color} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
      {/* Custom Legend below both charts */}
      <div className="custom-pie-legend" style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center', marginTop: 18 }}>
        {pieData.map((entry, idx) => (
          <div key={entry.name} style={{ display: 'flex', alignItems: 'center', margin: '0 12px 6px 0', fontSize: 14 }}>
            <span style={{ display: 'inline-block', width: 14, height: 14, background: entry.color, borderRadius: 3, marginRight: 6 }}></span>
            <span>{entry.name.charAt(0).toUpperCase() + entry.name.slice(1)} ({((entry.value / total) * 100).toFixed(0)}%)</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Dashboard; 