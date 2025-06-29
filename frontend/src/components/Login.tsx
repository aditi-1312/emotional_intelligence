import React, { useState, useEffect, useCallback } from 'react';
import './Login.css';

interface LoginProps {
  onLogin: (user: any) => void;
}

const Login: React.FC<LoginProps> = ({ onLogin }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isGoogleLoading, setIsGoogleLoading] = useState(false);

  const handleGoogleLogin = () => {
    setIsGoogleLoading(true);
    setError(null);
    
    console.log('Initiating Google OAuth login...');
    
    // Redirect to backend Google OAuth endpoint
    window.location.href = 'http://localhost:5001/auth/login';
  };

  const handleDemoLogin = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      console.log('Attempting demo login...');
      const response = await fetch('http://localhost:5001/auth/demo', {
        method: 'GET',
        credentials: 'include'
      });
      
      console.log('Demo login response status:', response.status);
      
      if (response.ok) {
        const data = await response.json();
        console.log('Demo login successful:', data);
        onLogin(data.user);
      } else {
        const errorData = await response.json().catch(() => ({}));
        console.error('Demo login failed:', errorData);
        setError('Demo login failed. Please try again.');
      }
    } catch (error) {
      console.error('Demo login error:', error);
      setError('Network error. Please check your connection.');
    } finally {
      setIsLoading(false);
    }
  };

  const checkAuthStatus = useCallback(async () => {
    try {
      const response = await fetch('http://localhost:5001/auth/user', {
        credentials: 'include'
      });
      
      if (response.ok) {
        const user = await response.json();
        onLogin(user);
      }
    } catch (error) {
      console.log('User not logged in');
    }
  }, [onLogin]);

  useEffect(() => {
    checkAuthStatus();
  }, [checkAuthStatus]);

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-header">
          <h1>🧠 Emotional Intelligence</h1>
          <p>Track your mood and gain insights</p>
        </div>
        
        <div className="login-body">
          <div className="login-options">
            <button 
              className="login-btn google-btn"
              onClick={handleGoogleLogin}
              disabled={isLoading || isGoogleLoading}
            >
              {isGoogleLoading ? (
                <span>Redirecting to Google...</span>
              ) : (
                <>
                  <svg className="google-icon" viewBox="0 0 24 24">
                    <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                    <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                    <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                    <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                  </svg>
                  Sign in with Google
                </>
              )}
            </button>
            
            <div className="login-divider">
              <span>or</span>
            </div>
            
            <button 
              className="login-btn demo-btn"
              onClick={handleDemoLogin}
              disabled={isLoading || isGoogleLoading}
            >
              {isLoading ? 'Logging in...' : 'Try Demo Mode'}
            </button>
          </div>
          
          {error && (
            <div className="error-message">
              {error}
            </div>
          )}
          
          <div className="login-info">
            <p><strong>Google Sign-in:</strong> Secure authentication using your Google account</p>
            <p><strong>Demo Mode:</strong> Test the app without Google authentication</p>
            <p>Your data will be stored locally for demonstration purposes.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login; 