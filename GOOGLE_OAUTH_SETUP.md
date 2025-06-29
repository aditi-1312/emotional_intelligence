# Google OAuth Setup Guide

## Overview

The Emotional Intelligence application supports Google OAuth for secure user authentication. This guide will help you set up and use Google OAuth login.

## ✅ Current Status

**Google OAuth is now working correctly!** The following issues have been resolved:

- ✅ Fixed SSL certificate issues
- ✅ Updated to use direct Google OAuth endpoints (no more 404 errors)
- ✅ Proper error handling and user feedback
- ✅ Demo login available for testing

## 🔧 Setup Instructions

### 1. Google OAuth Credentials

You already have Google OAuth credentials configured:
- **Client ID**: `486164293788-ut5inuq7jq6k7rdj3ueari3lmktpkpi5.apps.googleusercontent.com`
- **Client Secret**: Configured in `config.env`

### 2. Environment Configuration

Your `config.env` file should contain:
```env
GOOGLE_CLIENT_ID=486164293788-ut5inuq7jq6k7rdj3ueari3lmktpkpi5.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_client_secret_here
FLASK_SECRET_KEY=your_secret_key_here
```

### 3. Running the Application

1. **Start the backend:**
   ```bash
   source venv/bin/activate
   cd backend
   PORT=5001 python3 api.py
   ```

2. **Start the frontend:**
   ```bash
   cd frontend
   npm start
   ```

3. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5001

## 🔐 Login Options

### Option 1: Google OAuth Login (Recommended)

1. Click the **"Sign in with Google"** button on the login page
2. You'll be redirected to Google's authentication page
3. Sign in with your Google account
4. Grant permissions to the application
5. You'll be redirected back to the app and logged in

### Option 2: Demo Login (For Testing)

1. Click the **"Demo Login"** button on the login page
2. You'll be logged in as a demo user immediately
3. Perfect for testing the application without Google OAuth

## 🛠️ Troubleshooting

### Common Issues and Solutions

#### 1. "Google OAuth not configured" Error
- **Cause**: Missing or incorrect Google OAuth credentials
- **Solution**: Check your `config.env` file and ensure `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` are set correctly

#### 2. SSL Certificate Errors
- **Cause**: System SSL certificate issues
- **Solution**: The application now uses `certifi` for SSL certificate handling, which should resolve most SSL issues

#### 3. "404 Not Found" Errors
- **Cause**: Outdated Google OAuth discovery URL
- **Solution**: Fixed - now using direct Google OAuth endpoints

#### 4. Redirect URI Mismatch
- **Cause**: Google OAuth redirect URI doesn't match configured settings
- **Solution**: Ensure your Google OAuth app is configured for `http://localhost:5001/auth/callback`

### Testing the Setup

Run the test script to verify everything is working:
```bash
python3 test_google_oauth.py
```

Expected output:
```
🔍 Testing Google OAuth connectivity...
✅ GOOGLE_CLIENT_ID is set: 4861642937...
✅ GOOGLE_CLIENT_SECRET is set: GOCSPX-Fx-...
✅ Backend is running
✅ Google OAuth login endpoint working (redirecting to Google)
✅ Demo login working
📄 Demo user: Demo User

🎉 All Google OAuth tests passed!
```

## 🔒 Security Features

- **Secure Session Management**: Uses Flask-Login for secure user sessions
- **Database Storage**: User data is stored securely in SQLite database
- **SSL/TLS**: All OAuth communications use HTTPS
- **Token Validation**: Proper validation of Google OAuth tokens
- **User Verification**: Email verification through Google

## 📱 User Experience

### Login Flow
1. User clicks "Sign in with Google"
2. Redirected to Google's secure authentication page
3. User signs in with their Google account
4. Google redirects back to the application with an authorization code
5. Application exchanges code for user information
6. User is logged in and redirected to the dashboard

### User Data
- **Stored Information**: User ID, email, name, profile picture
- **Privacy**: Only basic profile information is stored
- **Security**: Passwords are never stored (handled by Google)

## 🚀 Production Deployment

For production deployment:

1. **Update Redirect URIs**: Change from `localhost` to your production domain
2. **Environment Variables**: Use production-grade secret keys
3. **Database**: Consider using PostgreSQL or MySQL instead of SQLite
4. **HTTPS**: Ensure all communications use HTTPS
5. **Domain Verification**: Verify your domain with Google OAuth

## 📞 Support

If you encounter any issues:

1. Check the backend logs for error messages
2. Run the test script: `python3 test_google_oauth.py`
3. Verify your Google OAuth credentials are correct
4. Ensure both backend and frontend are running

## 🎯 Summary

Google OAuth is now fully functional with:
- ✅ Secure authentication
- ✅ Proper error handling
- ✅ Demo login option
- ✅ Comprehensive testing
- ✅ User-friendly interface

You can now use either Google OAuth login or demo login to access the Emotional Intelligence application! 