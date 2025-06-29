import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate, useLocation } from 'react-router-dom';
import './App.css';
import Login from './components/Login';
import JournalEntry from './components/JournalEntry';
import Dashboard from './components/Dashboard';
import Timeline from './components/Timeline';
import Advice from './components/Advice';
import MoodCalendar from './components/MoodCalendar';
import { apiService } from './services/api';

interface User {
  id: number;
  email: string;
  name: string;
  picture: string;
}

function App() {
  const [user, setUser] = useState<User | null>(null);
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const [showRefreshModal, setShowRefreshModal] = useState(false);

  const handleLogin = (userData: User) => {
    setUser(userData);
  };

  const handleLogout = async () => {
    try {
      await fetch('http://localhost:5001/auth/logout', {
        credentials: 'include'
      });
    } catch (error) {
      console.error('Logout error:', error);
    }
    setUser(null);
  };

  const checkAuthStatus = async () => {
    try {
      console.log('Checking authentication status...');
      const response = await fetch('http://localhost:5001/auth/user', {
        credentials: 'include'
      });
      
      console.log('Auth check response status:', response.status);
      
      if (response.ok) {
        const userData = await response.json();
        console.log('User authenticated:', userData);
        setUser(userData);
      } else {
        // User is not authenticated, show login page
        console.log('User not authenticated, showing login page');
      }
    } catch (error) {
      console.error('Authentication check failed:', error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    checkAuthStatus();
  }, []);

  // Check for authentication success parameter in URL
  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const authParam = urlParams.get('auth');
    
    if (authParam === 'success') {
      console.log('Authentication success detected, checking user status...');
      // Remove the auth parameter from URL
      window.history.replaceState({}, document.title, window.location.pathname);
      // Check authentication status
      checkAuthStatus();
    }
  }, []);

  const handleEntryAdded = () => {
    setRefreshTrigger(prev => prev + 1);
  };

  if (isLoading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Loading...</p>
      </div>
    );
  }

  if (!user) {
    return <Login onLogin={handleLogin} />;
  }

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
            <div className="user-section">
              <div className="user-info">
                {user.picture && user.picture !== 'demo' ? (
                  <img src={user.picture} alt={user.name} className="user-avatar" />
                ) : (
                  <div className="user-avatar demo-avatar">
                    {user.name.charAt(0).toUpperCase()}
                  </div>
                )}
                <span className="user-name">{user.name}</span>
              </div>
              <button
                className="refresh-btn"
                onClick={() => {
                  console.log('Refresh button clicked');
                  setShowRefreshModal(true);
                }}
                style={{ 
                  marginRight: '0.5em', 
                  background: '#e74c3c', 
                  color: '#fff', 
                  border: 'none', 
                  padding: '0.5em 1.2em', 
                  borderRadius: '4px', 
                  fontWeight: 'bold', 
                  cursor: 'pointer',
                  transition: 'background-color 0.3s ease'
                }}
                onMouseEnter={(e) => e.currentTarget.style.background = '#c0392b'}
                onMouseLeave={(e) => e.currentTarget.style.background = '#e74c3c'}
              >
                🔄 Refresh
              </button>
              <button onClick={handleLogout} className="logout-btn">
                Logout
              </button>
            </div>
          </div>
        </nav>

        {/* Custom Refresh Modal */}
        {showRefreshModal && (
          <div 
            style={{
              position: 'fixed', 
              top: 0, 
              left: 0, 
              width: '100vw', 
              height: '100vh',
              background: 'rgba(0,0,0,0.5)', 
              zIndex: 9999, 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'center'
            }}
            onClick={(e) => {
              if (e.target === e.currentTarget) {
                setShowRefreshModal(false);
              }
            }}
          >
            <div style={{
              background: 'white', 
              borderRadius: 12, 
              padding: '2em', 
              minWidth: 320, 
              maxWidth: '90vw',
              boxShadow: '0 8px 32px rgba(0,0,0,0.3)', 
              textAlign: 'center'
            }}>
              <h2 style={{ color: '#e74c3c', marginBottom: 16 }}>⚠️ Refresh Confirmation</h2>
              <p style={{ marginBottom: 24, color: '#333', fontWeight: 500, lineHeight: 1.5 }}>
                <strong>Warning:</strong> This will reload the entire page and all your data will be lost!<br />
                This action cannot be undone.
              </p>
              <div style={{ display: 'flex', justifyContent: 'center', gap: 16, flexWrap: 'wrap' }}>
                <button
                  onClick={() => {
                    console.log('Refresh cancelled');
                    setShowRefreshModal(false);
                  }}
                  style={{ 
                    background: '#95a5a6', 
                    color: '#fff', 
                    border: 'none', 
                    padding: '0.75em 1.5em', 
                    borderRadius: 6, 
                    fontWeight: 500, 
                    cursor: 'pointer',
                    transition: 'background-color 0.3s ease'
                  }}
                  onMouseEnter={(e) => e.currentTarget.style.background = '#7f8c8d'}
                  onMouseLeave={(e) => e.currentTarget.style.background = '#95a5a6'}
                >
                  Cancel
                </button>
                <button
                  onClick={async () => {
                    console.log('Refresh confirmed, clearing data and reloading page...');
                    setShowRefreshModal(false);
                    try {
                      // Clear all journal entries
                      const response = await apiService.clearJournalEntries();
                      console.log('Data cleared successfully:', response.data);
                      
                      // Show success message briefly before reloading
                      alert(`Successfully cleared ${response.data.deleted_count} journal entries. The page will now reload.`);
                      
                      // Force reload the page
                      window.location.reload();
                    } catch (error) {
                      console.error('Error clearing data:', error);
                      alert('Failed to clear data. Please try again.');
                    }
                  }}
                  style={{ 
                    background: '#e74c3c', 
                    color: '#fff', 
                    border: 'none', 
                    padding: '0.75em 1.5em', 
                    borderRadius: 6, 
                    fontWeight: 600, 
                    cursor: 'pointer',
                    transition: 'background-color 0.3s ease'
                  }}
                  onMouseEnter={(e) => e.currentTarget.style.background = '#c0392b'}
                  onMouseLeave={(e) => e.currentTarget.style.background = '#e74c3c'}
                >
                  🔄 Yes, Refresh
                </button>
              </div>
            </div>
          </div>
        )}

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
