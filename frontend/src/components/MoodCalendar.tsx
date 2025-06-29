import React, { useState, useEffect } from 'react';
import { apiService, JournalEntry } from '../services/api';
import './MoodCalendar.css';

interface CalendarDay {
  date: Date;
  day: number;
  month: number;
  year: number;
  mood: string | null;
  journalEntry: string | null;
  isCurrentMonth: boolean;
  isToday: boolean;
}

const MoodCalendar: React.FC<{ refreshTrigger: number }> = ({ refreshTrigger }) => {
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
      joy: '😊',
      sadness: '😢',
      anger: '😠',
      fear: '😨',
      surprise: '😲',
      disgust: '🤢',
      love: '❤️',
      neutral: '😐'
    };
    return emojis[emotion] || '📝';
  };

  const fetchJournalEntries = async () => {
    setLoading(true);
    try {
      const response = await apiService.getJournalEntries(100);
      setJournalEntries(response.data);
    } catch (err) {
      setError('Failed to fetch journal entries');
      console.error('Error fetching journal entries:', err);
    } finally {
      setLoading(false);
    }
  };

  const generateCalendarDays = (date: Date, entries: JournalEntry[]): CalendarDay[] => {
    const year = date.getFullYear();
    const month = date.getMonth();
    
    // Get first day of month and last day of month
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    
    // Get the day of week for first day (0 = Sunday, 1 = Monday, etc.)
    const firstDayOfWeek = firstDay.getDay();
    
    // Get the last day of previous month to fill the grid
    const lastDayOfPrevMonth = new Date(year, month, 0);
    
    const days: CalendarDay[] = [];
    
    // Add days from previous month to fill the first week
    for (let i = firstDayOfWeek - 1; i >= 0; i--) {
      const day = lastDayOfPrevMonth.getDate() - i;
      const date = new Date(year, month - 1, day);
      days.push({
        date,
        day,
        month: month - 1,
        year,
        mood: null,
        journalEntry: null,
        isCurrentMonth: false,
        isToday: false
      });
    }
    
    // Add days of current month
    for (let day = 1; day <= lastDay.getDate(); day++) {
      const date = new Date(year, month, day);
      const today = new Date();
      const isToday = date.toDateString() === today.toDateString();
      
      // Find journal entry for this date
      const entry = entries.find(entry => {
        const entryDate = new Date(entry.timestamp);
        return entryDate.toDateString() === date.toDateString();
      });
      
      days.push({
        date,
        day,
        month,
        year,
        mood: entry?.dominant_emotion || null,
        journalEntry: entry?.text || null,
        isCurrentMonth: true,
        isToday
      });
    }
    
    // Add days from next month to fill the last week (if needed)
    const remainingDays = 42 - days.length; // 6 rows * 7 days = 42
    for (let day = 1; day <= remainingDays; day++) {
      const date = new Date(year, month + 1, day);
      days.push({
        date,
        day,
        month: month + 1,
        year,
        mood: null,
        journalEntry: null,
        isCurrentMonth: false,
        isToday: false
      });
    }
    
    return days;
  };

  useEffect(() => {
    fetchJournalEntries();
  }, [refreshTrigger]);

  useEffect(() => {
    setCalendarDays(generateCalendarDays(currentDate, journalEntries));
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
          {calendarDays.map((day, index) => (
            <div
              key={index}
              className={`calendar-day ${!day.isCurrentMonth ? 'other-month' : ''} ${day.isToday ? 'today' : ''} ${day.mood ? 'has-mood' : ''}`}
              onClick={() => setSelectedDay(day)}
              style={{
                backgroundColor: day.mood ? getEmotionColor(day.mood) : 'transparent',
                color: day.mood ? '#fff' : day.isCurrentMonth ? '#333' : '#ccc'
              }}
            >
              <div className="day-number">{day.day}</div>
              {day.mood && (
                <div className="mood-emoji">
                  {getEmotionEmoji(day.mood)}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {selectedDay && (
        <div className="day-details">
          <h3>{formatDate(selectedDay.date)}</h3>
          {selectedDay.mood ? (
            <div className="mood-info">
              <div className="mood-display">
                <span className="mood-emoji-large">{getEmotionEmoji(selectedDay.mood)}</span>
                <span className="mood-text">{selectedDay.mood.charAt(0).toUpperCase() + selectedDay.mood.slice(1)}</span>
              </div>
              {selectedDay.journalEntry && (
                <div className="journal-preview">
                  <h4>Journal Entry:</h4>
                  <p>{selectedDay.journalEntry.length > 150 
                    ? selectedDay.journalEntry.substring(0, 150) + '...' 
                    : selectedDay.journalEntry}</p>
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

      <div className="mood-legend">
        <h3>Mood Legend</h3>
        <div className="legend-items">
          {Object.entries({
            joy: '😊 Joy',
            love: '❤️ Love', 
            surprise: '😲 Surprise',
            neutral: '😐 Neutral',
            sadness: '😢 Sadness',
            fear: '😨 Fear',
            anger: '😠 Anger',
            disgust: '🤢 Disgust'
          }).map(([emotion, label]) => (
            <div key={emotion} className="legend-item">
              <div 
                className="legend-color" 
                style={{ backgroundColor: getEmotionColor(emotion) }}
              ></div>
              <span>{label}</span>
            </div>
          ))}
        </div>
      </div>

      {Object.keys(moodStats).length > 0 && (
        <div className="monthly-stats">
          <h3>This Month's Mood Summary</h3>
          <div className="stats-grid">
            {Object.entries(moodStats).map(([emotion, count]) => (
              <div key={emotion} className="stat-item">
                <div className="stat-emoji">{getEmotionEmoji(emotion)}</div>
                <div className="stat-details">
                  <div className="stat-emotion">{emotion.charAt(0).toUpperCase() + emotion.slice(1)}</div>
                  <div className="stat-count">{count} {count === 1 ? 'day' : 'days'}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default MoodCalendar; 