import React, { useState, useEffect } from 'react';
import { apiService, JournalEntry } from '../services/api';
import './MoodCalendar.css';

interface CalendarDay {
  date: Date | null;
  journalEntry: JournalEntry | null;
}

const MoodCalendar: React.FC = () => {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [calendarDays, setCalendarDays] = useState<CalendarDay[]>([]);
  const [journalEntries, setJournalEntries] = useState<JournalEntry[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [selectedDay, setSelectedDay] = useState<CalendarDay | null>(null);

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
    return colors[emotion] || '#E0E0E0';
  };

  const getEmotionEmoji = (emotion: string): string => {
    const emojis: Record<string, string> = {
      joy: '😄',
      sadness: '😢',
      anger: '😠',
      fear: '😨',
      surprise: '😲',
      disgust: '🤢',
      love: '❤️',
      neutral: '🙂'
    };
    return emojis[emotion] || '📝';
  };

  const fetchJournalEntries = async () => {
    setLoading(true);
    try {
      const response = await apiService.getJournalEntries();
      setJournalEntries(response.entries);
    } catch (err) {
      setError('Failed to fetch journal entries');
      console.error('Error fetching journal entries:', err);
    } finally {
      setLoading(false);
    }
  };

  const generateCalendarDays = () => {
    const days: CalendarDay[] = [];
    const firstDayOfMonth = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1);
    const lastDayOfMonth = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0);
    const startDay = firstDayOfMonth.getDay();
    const totalDays = lastDayOfMonth.getDate();
    const entries = Array.isArray(journalEntries) ? journalEntries : [];

    // Fill in days before the 1st of the month
    for (let i = 0; i < startDay; i++) {
      days.push({ date: null, journalEntry: null });
    }
    // Fill in days of the month
    for (let d = 1; d <= totalDays; d++) {
      const date = new Date(currentDate.getFullYear(), currentDate.getMonth(), d);
      const entry = entries.find(entry => {
        const entryDate = new Date(entry.timestamp);
        return (
          entryDate.getDate() === d &&
          entryDate.getMonth() === currentDate.getMonth() &&
          entryDate.getFullYear() === currentDate.getFullYear()
        );
      });
      days.push({ date, journalEntry: entry || null });
    }
    return days;
  };

  useEffect(() => {
    fetchJournalEntries();
  }, []);

  useEffect(() => {
    setCalendarDays(generateCalendarDays());
  }, [currentDate, journalEntries]);

  const goToPreviousMonth = () => {
    setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() - 1, 1));
  };

  const goToNextMonth = () => {
    setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 1));
  };

  const goToToday = () => {
    setCurrentDate(new Date());
  };

  const formatDate = (date: Date): string => {
    return date.toLocaleDateString('en-US', { 
      weekday: 'long', 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
  };

  const getMoodStats = () => {
    if (!Array.isArray(journalEntries)) return {};
    const currentMonthEntries = journalEntries.filter(entry => {
      const entryDate = new Date(entry.timestamp);
      return entryDate.getMonth() === currentDate.getMonth() && 
             entryDate.getFullYear() === currentDate.getFullYear();
    });

    const moodCounts: Record<string, number> = {};
    currentMonthEntries.forEach(entry => {
      const emotion = entry.dominant_emotion;
      moodCounts[emotion] = (moodCounts[emotion] || 0) + 1;
    });

    return moodCounts;
  };

  if (loading) {
    return (
      <div className="mood-calendar-container">
        <div className="loading">Loading your mood calendar...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="mood-calendar-container">
        <div className="error">{error}</div>
      </div>
    );
  }

  const moodStats = getMoodStats();
  const monthName = currentDate.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });

  // EMOTION MAP (for legend and summary)
  const EMOTION_MAP = [
    { name: 'Joy', color: '#ffe066', emoji: '😄' },
    { name: 'Love', color: '#ff4d9d', emoji: '❤️' },
    { name: 'Surprise', color: '#ffb3e6', emoji: '😲' },
    { name: 'Neutral', color: '#888888', emoji: '🙂' },
    { name: 'Sadness', color: '#4d90fe', emoji: '😢' },
    { name: 'Fear', color: '#8d5524', emoji: '😨' },
    { name: 'Anger', color: '#e63946', emoji: '😠' },
    { name: 'Disgust', color: '#388e3c', emoji: '🤢' },
  ];

  // Helper: Get summary for this month
  const getMonthlySummary = () => {
    if (!Array.isArray(journalEntries)) return {};
    const currentMonthEntries = journalEntries.filter(entry => {
      const entryDate = new Date(entry.timestamp);
      return entryDate.getMonth() === currentDate.getMonth() && 
             entryDate.getFullYear() === currentDate.getFullYear();
    });
    const summary: Record<string, number> = {};
    currentMonthEntries.forEach(entry => {
      const emotion = (entry.dominant_emotion || '').toLowerCase();
      summary[emotion] = (summary[emotion] || 0) + 1;
    });
    return summary;
  };

  return (
    <div className="mood-calendar-container">
      <h1>📅 Mood Calendar</h1>
      
      <div className="calendar-header">
        <button onClick={goToPreviousMonth} className="nav-button">
          ← Previous
        </button>
        <div className="current-month">
          <h2>{monthName}</h2>
          <button onClick={goToToday} className="today-button">
            Today
          </button>
        </div>
        <button onClick={goToNextMonth} className="nav-button">
          Next →
        </button>
      </div>

      <div className="calendar-grid">
        <div className="calendar-weekdays">
          <div>Sun</div>
          <div>Mon</div>
          <div>Tue</div>
          <div>Wed</div>
          <div>Thu</div>
          <div>Fri</div>
          <div>Sat</div>
        </div>
        
        <div className="calendar-days">
          {calendarDays.map((day, index) => {
            const mood = day.journalEntry?.dominant_emotion;
            const isCurrentMonth = day.date && day.date.getMonth() === currentDate.getMonth() && day.date.getFullYear() === currentDate.getFullYear();
            const isToday = day.date && (new Date()).toDateString() === day.date.toDateString();
            const dayNumber = day.date?.getDate();
            const entryText = day.journalEntry?.text || '';
            return (
              <div
                key={index}
                className={`calendar-day${!isCurrentMonth ? ' other-month' : ''}${isToday ? ' today' : ''}${mood ? ' has-mood' : ''}`}
                onClick={() => day.date && setSelectedDay(day)}
                style={{
                  backgroundColor: mood ? getEmotionColor(mood) : '#f4f6f8',
                  color: mood ? '#fff' : isCurrentMonth ? '#222' : '#bbb',
                  border: isToday ? '2px solid #ffd700' : undefined,
                  cursor: day.date ? 'pointer' : 'default',
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  justifyContent: 'center',
                  minHeight: 56,
                  minWidth: 56,
                  aspectRatio: '1 / 1',
                  borderRadius: 12,
                  boxShadow: '0 1px 4px rgba(0,0,0,0.04)',
                  padding: 0,
                  overflow: 'hidden',
                }}
              >
                <div className="day-number" style={{ fontWeight: 700, fontSize: 18, marginBottom: 2 }}>{dayNumber}</div>
                {mood && (
                  <>
                    <div className="mood-emoji" style={{ fontSize: 28, margin: '2px 0 2px 0' }}>{getEmotionEmoji(mood)}</div>
                    <div
                      className="calendar-entry-text"
                      style={{
                        fontSize: 12,
                        fontWeight: 400,
                        textAlign: 'center',
                        marginTop: 2,
                        maxWidth: '90%',
                        overflow: 'hidden',
                        textOverflow: 'ellipsis',
                        display: '-webkit-box',
                        WebkitLineClamp: 2,
                        WebkitBoxOrient: 'vertical',
                        whiteSpace: 'normal',
                        lineHeight: '1.2',
                        color: '#fff',
                      }}
                    >
                      {entryText}
                    </div>
                  </>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {selectedDay && (
        <div className="day-details">
          <h3>{selectedDay.date ? formatDate(selectedDay.date) : ''}</h3>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
            <button
              onClick={() => {
                const idx = calendarDays.findIndex(day => day.date && selectedDay.date && day.date.getTime() === selectedDay.date.getTime());
                for (let i = idx - 1; i >= 0; i--) {
                  if (calendarDays[i].journalEntry) {
                    setSelectedDay(calendarDays[i]);
                    break;
                  }
                }
              }}
              disabled={(() => {
                const idx = calendarDays.findIndex(day => day.date && selectedDay.date && day.date.getTime() === selectedDay.date.getTime());
                return idx === calendarDays.findIndex(day => day.journalEntry);
              })()}
              className="nav-button"
              style={{ marginRight: 12 }}
            >
              ← Previous Day
            </button>
            <button
              onClick={() => {
                const idx = calendarDays.findIndex(day => day.date && selectedDay.date && day.date.getTime() === selectedDay.date.getTime());
                for (let i = idx + 1; i < calendarDays.length; i++) {
                  if (calendarDays[i].journalEntry) {
                    setSelectedDay(calendarDays[i]);
                    break;
                  }
                }
              }}
              disabled={(() => {
                const idx = calendarDays.findIndex(day => day.date && selectedDay.date && day.date.getTime() === selectedDay.date.getTime());
                const lastIdx = calendarDays.map((d, i) => d.journalEntry ? i : -1).filter(i => i !== -1).slice(-1)[0];
                return idx === lastIdx;
              })()}
              className="nav-button"
              style={{ marginLeft: 12 }}
            >
              Next Day →
            </button>
          </div>
          {selectedDay.journalEntry?.dominant_emotion ? (
            <div className="mood-info">
              <div className="mood-display">
                <span className="mood-emoji-large">{getEmotionEmoji(selectedDay.journalEntry.dominant_emotion)}</span>
                <span className="mood-text">{selectedDay.journalEntry.dominant_emotion.charAt(0).toUpperCase() + selectedDay.journalEntry.dominant_emotion.slice(1)}</span>
              </div>
              {selectedDay.journalEntry && (
                <div className="journal-preview">
                  <h4>Journal Entry:</h4>
                  <p>{selectedDay.journalEntry.text.length > 150 
                    ? selectedDay.journalEntry.text.substring(0, 150) + '...' 
                    : selectedDay.journalEntry.text}</p>
                </div>
              )}
            </div>
          ) : (
            <div className="no-entry">
              <p>No journal entry for this day</p>
            </div>
          )}
          <button onClick={() => setSelectedDay(null)} className="close-button">
            Close
          </button>
        </div>
      )}

      {/* Mood Legend */}
      <div style={{
        background: '#fff',
        borderRadius: 18,
        boxShadow: '0 4px 24px rgba(0,0,0,0.07)',
        maxWidth: 1100,
        margin: '32px auto 0 auto',
        padding: '32px 32px 18px 32px',
        border: '1px solid #f0f0f0',
      }}>
        <h2 style={{ fontWeight: 700, fontSize: 32, marginBottom: 24, color: '#2d3748' }}>Mood Legend</h2>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: 32 }}>
          {EMOTION_MAP.map(e => (
            <div key={e.name} style={{ display: 'flex', alignItems: 'center', minWidth: 180, marginBottom: 16 }}>
              <span style={{
                display: 'inline-block',
                width: 32,
                height: 32,
                borderRadius: 8,
                background: e.color,
                marginRight: 12,
                border: '2px solid #f0f0f0',
                textAlign: 'center',
                fontSize: 22,
                lineHeight: '32px',
              }}>{e.emoji}</span>
              <span style={{ fontWeight: 600, fontSize: 20, color: '#222' }}>{e.name}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Mood Summary */}
      <div style={{
        background: '#fff',
        borderRadius: 18,
        boxShadow: '0 4px 24px rgba(0,0,0,0.10)',
        maxWidth: 1200,
        margin: '32px auto 0 auto',
        padding: '32px 32px 18px 32px',
        border: '1px solid #f0f0f0',
      }}>
        <h2 style={{ fontWeight: 700, fontSize: 32, marginBottom: 24, color: '#2d3748' }}>This Month's Mood Summary</h2>
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
            gap: '28px 32px',
            width: '100%',
            margin: '0 auto',
          }}
        >
          {EMOTION_MAP.map(e => {
            const count = getMonthlySummary()[e.name.toLowerCase()] || 0;
            return (
              <div
                key={e.name}
                style={{
                  background: '#fff',
                  borderRadius: 14,
                  minWidth: 180,
                  maxWidth: 260,
                  padding: '18px 24px',
                  boxShadow: '0 4px 16px rgba(0,0,0,0.08)',
                  borderLeft: `4px solid ${e.color}`,
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'flex-start',
                  justifyContent: 'center',
                }}
              >
                <span style={{ fontSize: 28, marginBottom: 6, color: '#222', fontWeight: 700 }}>
                  {e.emoji} <span style={{ fontWeight: 700, fontSize: 22, color: '#222', marginLeft: 8 }}>{e.name}</span>
                </span>
                <span style={{ fontSize: 18, color: count === 0 ? '#888' : '#444', marginLeft: 4, fontWeight: 500 }}>
                  {count} {count === 1 ? 'day' : 'days'}
                </span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default MoodCalendar; 