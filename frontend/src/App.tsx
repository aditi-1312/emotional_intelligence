import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from 'react-router-dom';
import './App.css';
import JournalEntry from './components/JournalEntry';
import Dashboard from './components/Dashboard';
import Timeline from './components/Timeline';
import Advice from './components/Advice';
import MoodCalendar from './components/MoodCalendar';

function App() {
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleEntryAdded = () => {
    setRefreshTrigger(prev => prev + 1);
  };

  return (
    <Router>
      <div className="App">
        <nav className="navbar">
          <div className="nav-container">
            <h1 className="nav-title">😊 Mood Tracker</h1>
            <div className="nav-links">
              <Link to="/" className="nav-link">📝 Journal</Link>
              <Link to="/dashboard" className="nav-link">📊 Dashboard</Link>
              <Link to="/timeline" className="nav-link">📈 Timeline</Link>
              <Link to="/calendar" className="nav-link">📅 Calendar</Link>
              <Link to="/advice" className="nav-link">🧠 Advice</Link>
            </div>
          </div>
        </nav>

        <main className="main-content">
          <Routes>
            <Route path="/" element={<JournalEntry onEntryAdded={handleEntryAdded} />} />
            <Route path="/dashboard" element={<Dashboard refreshTrigger={refreshTrigger} />} />
            <Route path="/timeline" element={<Timeline refreshTrigger={refreshTrigger} />} />
            <Route path="/calendar" element={<MoodCalendar refreshTrigger={refreshTrigger} />} />
            <Route path="/advice" element={<Advice refreshTrigger={refreshTrigger} />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
