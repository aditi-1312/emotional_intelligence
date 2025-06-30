import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { apiService, TimelineEntry } from '../services/api';
import './Timeline.css';

const Timeline: React.FC = () => {
  const [timeline, setTimeline] = useState<TimelineEntry[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchTimeline = async () => {
    setLoading(true);
    setError('');
    
    try {
      const timelineData = await apiService.getTimeline();
      setTimeline(timelineData);
    } catch (err) {
      setError('Failed to load timeline. Please try again.');
      console.error('Error fetching timeline:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTimeline();
  }, []);

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

  const getEmotionEmoji = (emotion: string) => {
    const emojis: Record<string, string> = {
      joy: '😄',
      love: '❤️',
      sadness: '😢',
      anger: '😠',
      fear: '😨',
      surprise: '😲',
      disgust: '🤢',
      neutral: '🙂'
    };
    return emojis[emotion] || '🙂';
  };

  const chartData = timeline
    .map(entry => {
      // Use 'emotion' if present (from backend), else fallback to 'dominant_emotion' (old frontend type)
      const emotion = entry.emotion || entry.dominant_emotion || '';
      return {
        date: new Date(entry.timestamp).toLocaleDateString('en-US', { 
          month: 'short', 
          day: 'numeric' 
        }),
        emotion,
        value: getEmotionValue(emotion),
        text: entry.text,
        color: getEmotionColor(emotion),
        confidence: entry.confidence,
        fullDate: entry.timestamp
      };
    })
    .sort((a, b) => new Date(a.fullDate).getTime() - new Date(b.fullDate).getTime()); // Sort by date ascending

  if (loading) {
    return (
      <div className="timeline-container">
        <div className="loading">Loading timeline...</div>
      </div>
    );
  }

  // Only show error if there was a real fetch error and not just empty data
  if (error && timeline.length === 0) {
    return (
      <div className="timeline-container">
        <div className="error-message">{error}</div>
        <div className="no-data">
          <p>No journal entries found. Start writing in your journal to see your mood timeline!</p>
        </div>
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

      {/* Only show error if there is data and an error (rare) */}
      {error && timeline.length > 0 && (
        <div className="error-message">{error}</div>
      )}

      {timeline.length === 0 && !loading && !error && (
        <div className="no-data">
          <p>No journal entries found. Start writing in your journal to see your mood timeline!</p>
        </div>
      )}

      {timeline.length > 0 && (
        <div className="timeline-content">
          {/* Mood Chart */}
          <div className="chart-section">
            <h3>Mood Over Time</h3>
            <ResponsiveContainer width="100%" height={320}>
              <LineChart data={chartData} margin={{ top: 30, right: 30, left: 10, bottom: 10 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis 
                  dataKey="date" 
                  tick={{ fontSize: 13, fontWeight: 500 }}
                  axisLine={{ stroke: '#ccc' }}
                  padding={{ left: 10, right: 10 }}
                />
                <YAxis 
                  domain={[0, 7]}
                  ticks={[0, 1, 2, 3, 4, 5, 6, 7]}
                  tickFormatter={(value) => {
                    const emotions = ['Disgust', 'Anger', 'Fear', 'Sadness', 'Neutral', 'Surprise', 'Love', 'Joy'];
                    return emotions[value] || '';
                  }}
                  tick={{ fontSize: 13, fontWeight: 500 }}
                  axisLine={{ stroke: '#ccc' }}
                  width={90}
                />
                <Tooltip 
                  content={({ active, payload, label }) => {
                    if (active && payload && payload.length) {
                      const data = payload[0].payload;
                      return (
                        <div className="custom-tooltip" style={{ background: '#fff', border: '1px solid #eee', borderRadius: 8, padding: 12 }}>
                          <div style={{ fontWeight: 700, fontSize: 15, marginBottom: 4 }}>{label}</div>
                          <div style={{ color: data.color, fontWeight: 700, fontSize: 16, marginBottom: 2 }}>
                            {getEmotionEmoji(data.emotion)} {data.emotion ? data.emotion.toUpperCase() : ''}
                          </div>
                          <div style={{ fontSize: 14, color: '#888', marginBottom: 2 }}>Confidence: {(data.confidence * 100).toFixed(1)}%</div>
                          <div style={{ fontSize: 14, color: '#333' }}>{data.text}</div>
                        </div>
                      );
                    }
                    return null;
                  }}
                />
                <Line 
                  type="monotoneX" 
                  dataKey="value" 
                  stroke="#667eea" 
                  strokeWidth={3}
                  dot={({ cx, cy, payload }) => (
                    <circle
                      cx={cx}
                      cy={cy}
                      r={7}
                      fill={getEmotionColor(payload.emotion)}
                      stroke="#fff"
                      strokeWidth={2}
                    />
                  )}
                  activeDot={{ r: 10, stroke: '#fff', strokeWidth: 3 }}
                  isAnimationActive={true}
                />
              </LineChart>
            </ResponsiveContainer>
            {/* Custom Legend */}
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 18, marginTop: 18, justifyContent: 'center' }}>
              {['joy', 'love', 'surprise', 'neutral', 'sadness', 'fear', 'anger', 'disgust'].map(emotion => (
                <div key={emotion} style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                  <span style={{ fontSize: 20 }}>{getEmotionEmoji(emotion)}</span>
                  <span style={{ color: getEmotionColor(emotion), fontWeight: 600, fontSize: 15 }}>{emotion.charAt(0).toUpperCase() + emotion.slice(1)}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Timeline List */}
          <div style={{ display: 'flex', justifyContent: 'center', marginTop: 32, marginBottom: 32 }}>
            <div style={{
              background: '#f8fafc',
              borderRadius: 18,
              boxShadow: '0 4px 24px rgba(0,0,0,0.07)',
              maxWidth: 900,
              width: '100%',
              padding: '32px 32px 18px 32px',
              border: '1px solid #f0f0f0',
            }}>
              <h3 style={{ fontWeight: 700, fontSize: 26, marginBottom: 28, marginLeft: 2, color: '#222', textAlign: 'left' }}>Recent Entries</h3>
              <div className="entries-container">
                {timeline.map((entry, index) => {
                  const emotion = entry.dominant_emotion || entry.emotion || '';
                  return (
                    <div key={entry.id} className="timeline-entry-card" style={{ display: 'flex', alignItems: 'center', background: '#fff', borderRadius: 14, boxShadow: '0 2px 8px rgba(0,0,0,0.04)', marginBottom: 28, padding: '18px 24px', minHeight: 60 }}>
                      {/* Emotion pill with color and label */}
                      <div style={{
                        background: getEmotionColor(emotion),
                        color: '#fff',
                        fontWeight: 700,
                        borderRadius: 8,
                        padding: '6px 28px',
                        marginRight: 22,
                        fontSize: 18,
                        minWidth: 70,
                        textAlign: 'center',
                        letterSpacing: 1.2,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                      }}>
                        {emotion ? emotion.toUpperCase() : '—'}
                      </div>
                      {/* Entry text */}
                      <div style={{ flex: 1, fontSize: 20, color: '#222', fontWeight: 600, textAlign: 'left' }}>
                        {entry.text}
                      </div>
                      {/* Confidence */}
                      <div style={{ fontWeight: 700, fontSize: 18, color: '#888', marginLeft: 18, minWidth: 70, textAlign: 'right' }}>
                        {(entry.confidence * 100).toFixed(1)}%
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>

          {/* Emotion Scale below Recent Entries */}
          <div style={{ display: 'flex', justifyContent: 'center', marginBottom: 32 }}>
            <div style={{
              background: '#f8fafc',
              borderRadius: 18,
              boxShadow: '0 4px 24px rgba(0,0,0,0.07)',
              maxWidth: 1100,
              width: '100%',
              padding: '28px 32px 28px 32px',
              border: '1px solid #f0f0f0',
            }}>
              <h3 style={{ fontWeight: 700, fontSize: 26, marginBottom: 24, color: '#222', textAlign: 'center' }}>Emotion Scale</h3>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 24, justifyContent: 'center' }}>
                {['joy', 'love', 'surprise', 'neutral', 'sadness', 'fear', 'anger', 'disgust'].map(emotion => (
                  <div key={emotion} style={{
                    display: 'flex', alignItems: 'center', background: '#fff', borderRadius: 12, boxShadow: '0 1px 6px rgba(0,0,0,0.04)', padding: '10px 32px 10px 18px', minWidth: 160, marginBottom: 8, border: '1px solid #f0f0f0', fontWeight: 700, fontSize: 20
                  }}>
                    <span style={{
                      display: 'inline-block',
                      width: 28,
                      height: 28,
                      borderRadius: 6,
                      background: getEmotionColor(emotion),
                      marginRight: 16,
                      border: '2px solid #f8fafc'
                    }}></span>
                    <span style={{ color: '#222', fontWeight: 700, fontSize: 20 }}>{emotion.toUpperCase()}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Timeline; 