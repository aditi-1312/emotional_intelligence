import React, { useState } from 'react';
import { apiService } from '../services/api';
import './JournalEntry.css';

interface JournalEntryProps {
  onEntryAdded?: () => void;
}

const JournalEntry: React.FC<JournalEntryProps> = ({ onEntryAdded }) => {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [analysis, setAnalysis] = useState<any>(null);
  const [message, setMessage] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!text.trim()) return;

    setLoading(true);
    setMessage('');
    setAnalysis(null);

    try {
      const response = await apiService.addJournalEntry(text);
      setAnalysis(response.data.analysis);
      setMessage('Journal entry saved successfully!');
      setText('');
      
      // Notify parent component
      if (onEntryAdded) {
        onEntryAdded();
      }
    } catch (error) {
      setMessage('Error saving journal entry. Please try again.');
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const getEmotionColor = (emotion: string) => {
    const colors: Record<string, string> = {
      joy: '#FFD700',
      love: '#FF69B4',
      sadness: '#87CEEB',
      anger: '#FF6347',
      fear: '#8A2BE2',
      surprise: '#FFA500',
      neutral: '#808080'
    };
    return colors[emotion] || '#808080';
  };

  return (
    <div className="journal-container">
      <div className="journal-header">
        <h2>📝 Daily Journal Entry</h2>
        <p>Write about your day and discover your emotional patterns</p>
      </div>

      <form onSubmit={handleSubmit} className="journal-form">
        <div className="form-group">
          <label htmlFor="journalText">How are you feeling today?</label>
          <textarea
            id="journalText"
            value={text}
            onChange={(e) => setText(e.target.value)}
            className="form-textarea"
            placeholder="Write about your day, your feelings, or anything on your mind..."
            rows={6}
            required
          />
        </div>

        <button type="submit" className="submit-btn" disabled={loading}>
          {loading ? 'Analyzing...' : 'Save & Analyze'}
        </button>
      </form>

      {message && (
        <div className={`message ${message.includes('Error') ? 'error' : 'success'}`}>
          {message}
        </div>
      )}

      {analysis && (
        <div className="analysis-result">
          <h3>🎯 Emotion Analysis</h3>
          <div className="emotion-card">
            <div 
              className="dominant-emotion"
              style={{ backgroundColor: getEmotionColor(analysis.emotion) }}
            >
              <h4>{analysis.emotion.toUpperCase()}</h4>
              <p>Confidence: {(analysis.confidence * 100).toFixed(1)}%</p>
            </div>
          </div>

          {analysis.emotions && (
            <div className="emotion-breakdown">
              <h4>Emotion Distribution:</h4>
              <div className="emotion-bars">
                {Object.entries(analysis.emotions).map(([emotion, score]: [string, any]) => (
                  <div key={emotion} className="emotion-bar">
                    <span className="emotion-label">{emotion}</span>
                    <div className="bar-container">
                      <div 
                        className="bar-fill"
                        style={{ 
                          width: `${score * 100}%`,
                          backgroundColor: getEmotionColor(emotion)
                        }}
                      />
                    </div>
                    <span className="emotion-score">{(score * 100).toFixed(1)}%</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default JournalEntry; 