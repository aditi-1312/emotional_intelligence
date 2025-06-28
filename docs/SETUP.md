# 🚀 Mood Tracker Setup Guide

This guide will help you set up the Mood Tracker application with Google OAuth authentication and persistent database storage.

## 📋 Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn
- Google account for OAuth setup

## 🔧 Installation

### 1. Clone and Install Dependencies

```bash
# Install Python dependencies
python3 -m pip install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install
cd ..
```

### 2. Set Up Google OAuth

#### Option A: Use the Setup Script (Recommended)

```bash
python3 setup_google_oauth.py
```

This interactive script will:
- Guide you through Google OAuth setup
- Create the config.env template
- Open Google Cloud Console in your browser

#### Option B: Manual Setup

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com/
   - Create a new project or select existing one

2. **Enable Google+ API**
   - Go to "APIs & Services" > "Library"
   - Search for "Google+ API" and enable it

3. **Create OAuth 2.0 Credentials**
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth 2.0 Client IDs"
   - Choose "Web application"

4. **Configure OAuth Consent Screen**
   - App name: "Mood Tracker"
   - User support email: your email
   - Developer contact information: your email

5. **Add Authorized Redirect URIs**
   - `http://localhost:5001/auth/google/callback`
   - `https://yourdomain.com/auth/google/callback` (for production)

6. **Copy Credentials**
   - Copy the Client ID and Client Secret
   - Add them to your `config.env` file

### 3. Configure Environment Variables

Create a `config.env` file in the root directory:

```env
# Flask Configuration
FLASK_SECRET_KEY=your-secret-key-here-change-this
FLASK_ENV=development

# Database Configuration
DATABASE_URL=sqlite:///emotional_intelligence.db

# Google OAuth Configuration
GOOGLE_CLIENT_ID=your-google-client-id-here
GOOGLE_CLIENT_SECRET=your-google-client-secret-here
GOOGLE_DISCOVERY_URL=https://accounts.google.com/.well-known/openid_configuration

# Application Configuration
FRONTEND_URL=http://localhost:3000
API_URL=http://localhost:5001
```

## 🚀 Running the Application

### 1. Start the Backend API

```bash
python3 api.py
```

The API will run on `http://localhost:5001`

### 2. Start the Frontend

```bash
cd frontend
npm start
```

The frontend will run on `http://localhost:3000`

### 3. Access the Application

1. Open your browser and go to `http://localhost:3000`
2. Click "Continue with Google" to sign in
3. Grant permissions to the application
4. Start tracking your emotions!

## 🗄️ Database

The application uses SQLite by default for easy setup. The database file (`emotional_intelligence.db`) will be created automatically when you first run the application.

### Database Features:
- **User Management**: Secure user authentication with Google OAuth
- **Journal Entries**: Persistent storage of all journal entries
- **Emotion Analysis**: Stored analysis results for each entry
- **Analytics**: Historical data for mood tracking and patterns

### Data Persistence:
- ✅ All data is saved to the database
- ✅ Data persists between application restarts
- ✅ Each user has their own private data
- ✅ No data is lost when the server restarts

## 🔒 Security Features

- **Google OAuth**: Secure authentication with Google accounts
- **Session Management**: Flask-Login handles user sessions
- **Data Isolation**: Each user can only access their own data
- **HTTPS Ready**: Configured for production HTTPS deployment

## 🛠️ Development

### Project Structure:
```
emotional_intelligence/
├── api.py                 # Main Flask API
├── models.py              # Database models
├── config.env             # Environment variables
├── setup_google_oauth.py  # OAuth setup script
├── frontend/              # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── services/      # API services
│   │   └── App.tsx        # Main app component
│   └── package.json
└── requirements.txt       # Python dependencies
```

### Key Features:
- **Authentication**: Google OAuth login/logout
- **Journal Entries**: Add and view emotional journal entries
- **Emotion Analysis**: AI-powered emotion detection
- **Analytics Dashboard**: Visual charts and statistics
- **Timeline View**: Historical mood tracking
- **Current Mood Display**: Shows latest emotional state

## 🚀 Production Deployment

For production deployment:

1. **Update Environment Variables**:
   - Set `FLASK_ENV=production`
   - Use a strong `FLASK_SECRET_KEY`
   - Update `FRONTEND_URL` and `API_URL` to your domain

2. **Database**:
   - Consider using PostgreSQL for production
   - Set up database backups

3. **Security**:
   - Use HTTPS
   - Set up proper CORS configuration
   - Configure Google OAuth for your domain

4. **Deployment Options**:
   - Heroku
   - AWS
   - Google Cloud Platform
   - DigitalOcean

## 🆘 Troubleshooting

### Common Issues:

1. **Google OAuth Error**:
   - Check that redirect URIs are correct
   - Verify Client ID and Secret in config.env
   - Ensure Google+ API is enabled

2. **Database Issues**:
   - Check file permissions for database file
   - Ensure SQLite is installed

3. **Frontend Not Loading**:
   - Check that both API and frontend are running
   - Verify CORS configuration
   - Check browser console for errors

### Getting Help:

- Check the browser console for frontend errors
- Check the API logs for backend errors
- Verify all environment variables are set correctly

## 🎉 Success!

Once everything is set up, you'll have a fully functional mood tracking application with:

- ✅ Secure Google OAuth authentication
- ✅ Persistent database storage
- ✅ Real-time emotion analysis
- ✅ Beautiful analytics dashboard
- ✅ Mobile-responsive design
- ✅ Data that never gets lost

Happy mood tracking! 😊 