import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { apiService, TimelineEntry } from '../services/api';
import './Timeline.css';

const Timeline: React.FC<{ refreshTrigger: number }> = ({ refreshTrigger }) => {
  const [timeline, setTimeline] = useState<TimelineEntry[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchTimeline = async () => {
    setLoading(true);
    setError('');
    
    try {
      const response = await apiService.getTimeline();
      setTimeline(response.data);
    } catch (err) {
      setError('Failed to load timeline. Please try again.');
      console.error('Error fetching timeline:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTimeline();
  }, [refreshTrigger]);

  const getEmotionColor = (emotion: string) => {
    const colors: Record<string, string> = {
      joy: '#FFD700',
      love: '#FF69B4',
      sadness: '#87CEEB',
      anger: '#FF6347',
      fear: '#8A2BE2',
      surprise: '#FFA500',
      disgust: '#228B22',
      neutral: '#808080'
    };
    return colors[emotion] || '#808080';
  };

  const getEmotionValue = (emotion: string) => {
    const values: Record<string, number> = {
      joy: 7,
      love: 6,
      surprise: 5,
      neutral: 4,
      sadness: 3,
      fear: 2,
      anger: 1,
      disgust: 0
    };
    return values[emotion] || 4;
  };

  const chartData = timeline
    .map(entry => ({
      date: new Date(entry.timestamp).toLocaleDateString('en-US', { 
        month: 'short', 
        day: 'numeric' 
      }),
      emotion: entry.dominant_emotion,
      value: getEmotionValue(entry.dominant_emotion),
      text: entry.text,
      color: getEmotionColor(entry.dominant_emotion),
      confidence: entry.confidence,
      fullDate: entry.timestamp
    }))
    .sort((a, b) => new Date(a.fullDate).getTime() - new Date(b.fullDate).getTime()); // Sort by date ascending

  if (loading) {
    return (
      <div className="timeline-container">
        <div className="loading">Loading timeline...</div>
      </div>
    );
  }

  return (
    <div className="timeline-container">
      <div className="timeline-header">
        <h2>📈 Mood Timeline</h2>
        <button onClick={fetchTimeline} className="refresh-btn">
          🔄 Refresh
        </button>
      </div>

      {error && (
        <div className="error-message">{error}</div>
      )}

      {timeline.length === 0 && !loading && (
        <div className="no-data">
          <p>No journal entries found. Start writing in your journal to see your mood timeline!</p>
        </div>
      )}

      {timeline.length > 0 && (
        <div className="timeline-content">
          {/* Mood Chart */}
          <div className="chart-section">
            <h3>Mood Over Time</h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis 
                  dataKey="date" 
                  tick={{ fontSize: 12 }}
                  axisLine={{ stroke: '#ccc' }}
                />
                <YAxis 
                  domain={[0, 7]}
                  ticks={[0, 1, 2, 3, 4, 5, 6, 7]}
                  tickFormatter={(value) => {
                    const emotions = ['Disgust', 'Anger', 'Fear', 'Sadness', 'Neutral', 'Surprise', 'Love', 'Joy'];
                    return emotions[value] || '';
                  }}
                  tick={{ fontSize: 11 }}
                  axisLine={{ stroke: '#ccc' }}
                />
                <Tooltip 
                  content={({ active, payload, label }) => {
                    if (active && payload && payload.length) {
                      const data = payload[0].payload;
                      return (
                        <div className="custom-tooltip">
                          <p className="tooltip-date">{label}</p>
                          <p className="tooltip-emotion" style={{ color: data.color, fontWeight: 'bold' }}>
                            {data.emotion.toUpperCase()}
                          </p>
                          <p className="tooltip-confidence">
                            Confidence: {(data.confidence * 100).toFixed(1)}%
                          </p>
                          <p className="tooltip-text">{data.text}</p>
                        </div>
                      );
                    }
                    return null;
                  }}
                />
                <Line 
                  type="monotone" 
                  dataKey="value" 
                  stroke="#667eea" 
                  strokeWidth={3}
                  dot={(props) => {
                    const { cx, cy, payload } = props;
                    return (
                      <circle
                        cx={cx}
                        cy={cy}
                        r={6}
                        fill={payload.color}
                        stroke="#fff"
                        strokeWidth={2}
                      />
                    );
                  }}
                  activeDot={{ r: 8, stroke: '#fff', strokeWidth: 2 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Timeline List */}
          <div className="timeline-list">
            <h3>Recent Entries</h3>
            <div className="entries-container">
              {timeline.map((entry, index) => (
                <div key={entry.id} className="timeline-entry">
                  <div className="entry-header">
                    <div 
                      className="emotion-indicator"
                      style={{ backgroundColor: getEmotionColor(entry.dominant_emotion) }}
                    >
                      {entry.dominant_emotion.toUpperCase()}
                    </div>
                    <span className="entry-date">
                      {entry.date}
                    </span>
                    <span className="entry-confidence">
                      {(entry.confidence * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="entry-text">
                    {entry.text}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Emotion Legend */}
          <div className="emotion-legend">
            <h3>Emotion Scale</h3>
            <div className="legend-items">
              {['joy', 'love', 'surprise', 'neutral', 'sadness', 'fear', 'anger', 'disgust'].map(emotion => (
                <div key={emotion} className="legend-item">
                  <div 
                    className="legend-color"
                    style={{ backgroundColor: getEmotionColor(emotion) }}
                  />
                  <span className="legend-label">{emotion.toUpperCase()}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Timeline; 