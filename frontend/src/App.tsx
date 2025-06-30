import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Link, useLocation } from 'react-router-dom';
import './App.css';

import Dashboard from './components/Dashboard';
import JournalEntry from './components/JournalEntry';
import Timeline from './components/Timeline';
import MoodCalendar from './components/MoodCalendar';
import Advice from './components/Advice';

const navItems = [
  { path: '/journal', label: 'Journal', icon: '📝' },
  { path: '/dashboard', label: 'Dashboard', icon: '📊' },
  { path: '/timeline', label: 'Timeline', icon: '📈' },
  { path: '/calendar', label: 'Calendar', icon: '📅' },
  { path: '/advice', label: 'Advice', icon: '🧠' },
];

const NavBar: React.FC = () => {
  const location = useLocation();
  return (
    <nav className="navbar">
      <div className="navbar-left">
        <span className="app-logo">😊</span>
        <span className="app-title">Mood<br/>Tracker</span>
      </div>
      <div className="navbar-center">
        {navItems.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={`nav-link${location.pathname === item.path ? ' active' : ''}`}
          >
            <span className="nav-icon">{item.icon}</span> {item.label}
          </Link>
        ))}
      </div>
      <div className="navbar-right">
        <span className="user-badge">D</span>
        <span className="user-label">Demo User</span>
        <button className="refresh-btn">Refresh</button>
        <button className="logout-btn">Logout</button>
      </div>
    </nav>
  );
};

const Card: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div className="main-card">{children}</div>
);

function App() {
  return (
    <Router>
      <div className="app-bg">
        <NavBar />
        <div className="main-content">
          <Routes>
            <Route path="/" element={<Navigate to="/journal" />} />
            <Route path="/journal" element={<Card><JournalEntry /></Card>} />
            <Route path="/dashboard" element={<Card><Dashboard /></Card>} />
            <Route path="/timeline" element={<Card><Timeline /></Card>} />
            <Route path="/calendar" element={<Card><MoodCalendar /></Card>} />
            <Route path="/advice" element={<Card><Advice /></Card>} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
