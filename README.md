# 🧠 Emotional Intelligence Mood Tracker

A comprehensive web application for tracking emotional well-being using AI-powered emotion analysis and personalized insights.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![React](https://img.shields.io/badge/React-18.0+-blue.svg)
![TypeScript](https://img.shields.io/badge/TypeScript-4.0+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Features

### 📝 **Journal Entry System**
- Write daily mood entries with natural language
- AI-powered emotion detection from text
- Confidence scoring for emotion analysis
- Timestamp tracking for emotional journey

### 📊 **Analytics Dashboard**
- Visual representation of mood trends
- Emotion distribution charts
- Statistical analysis of emotional patterns
- Real-time data aggregation

### 📈 **Timeline View**
- Chronological view of emotional journey
- Filter and search through entries
- Visual timeline with emotion indicators
- Historical mood tracking

### 📅 **Mood Calendar**
- Calendar-based mood tracking
- Monthly and weekly views
- Color-coded emotion indicators
- Quick entry creation

### 🤖 **AI Insights**
- OpenAI GPT-3.5 powered insights
- Personalized emotional intelligence advice
- Context-aware suggestions
- Rule-based fallback system

### 🔐 **Secure Authentication**
- Google OAuth 2.0 integration
- Secure user session management
- Data isolation per user
- Demo login for testing

### 🗂️ **Data Management**
- Refresh/clear functionality
- Export capabilities
- Data backup and restore
- User data privacy controls

## 🛠️ Technology Stack

### **Backend**
- **Python Flask** - Web framework
- **SQLite** - Database
- **Flask-Login** - Authentication
- **OAuthlib** - Google OAuth integration
- **OpenAI API** - AI insights
- **Pandas/NumPy** - Data processing

### **Frontend**
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Axios** - HTTP client
- **React Router** - Navigation
- **CSS3** - Styling

### **DevOps**
- **Docker** - Containerization
- **Git** - Version control
- **Python venv** - Environment management
- **npm** - Package management

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn
- Google OAuth credentials

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/emotional-intelligence-mood-tracker.git
cd emotional-intelligence-mood-tracker
```

### 2. Backend Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp config.env.example config.env
# Edit config.env with your credentials
```

### 3. Frontend Setup
```bash
cd frontend
npm install
```

### 4. Configure Google OAuth
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URIs:
   - `http://localhost:5001/auth/callback`
6. Update `config.env` with your credentials

### 5. Run the Application
```bash
# Terminal 1: Start backend
cd backend
python api.py

# Terminal 2: Start frontend
cd frontend
npm start
```

### 6. Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:5001
- Health Check: http://localhost:5001/health

## 📁 Project Structure

```
emotional-intelligence-mood-tracker/
├── backend/                 # Flask backend
│   ├── api.py              # Main Flask application
│   ├── config.py           # Configuration management
│   ├── models.py           # Database models
│   └── src/
│       ├── data_processor.py  # Text processing
│       ├── models.py          # AI models
│       └── utils.py           # Utility functions
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── services/       # API services
│   │   └── App.tsx         # Main application
│   ├── package.json
│   └── tsconfig.json
├── data_and_models/        # Data storage and ML models
├── docs/                   # Documentation
├── scripts/                # Utility scripts
├── tests/                  # Test files
├── config.env.example      # Environment template
├── requirements.txt        # Python dependencies
├── docker-compose.yml      # Docker configuration
└── README.md              # This file
```

## 🔧 Configuration

### Environment Variables
Create a `config.env` file with the following variables:

```env
# Google OAuth
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

# Flask
FLASK_SECRET_KEY=your_secret_key

# OpenAI (Optional)
OPENAI_API_KEY=your_openai_api_key

# Database
DATABASE_URL=sqlite:///instance/emotional_intelligence.db

# CORS
CORS_ORIGINS=http://localhost:3000
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
python -m pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

### API Testing
```bash
# Test health endpoint
curl http://localhost:5001/health

# Test OAuth flow
curl -I http://localhost:5001/auth/login
```

## 📊 API Endpoints

### Authentication
- `GET /auth/login` - Initiate Google OAuth
- `GET /auth/callback` - OAuth callback handler
- `GET /auth/user` - Get current user
- `GET /auth/logout` - Logout user
- `GET /auth/demo` - Demo login

### Journal Entries
- `POST /journal` - Add new journal entry
- `GET /journal` - Get journal entries
- `DELETE /journal/clear` - Clear all entries

### Analytics
- `GET /analytics/summary` - Get analytics summary
- `GET /analytics/timeline` - Get timeline data

### AI Insights
- `POST /ai/insights` - Get AI-powered insights
- `GET /suggestions` - Get wellness suggestions

## 🐳 Docker Deployment

### Using Docker Compose
```bash
docker-compose up -d
```

### Manual Docker Build
```bash
# Build backend
docker build -t emotional-intelligence-backend .

# Build frontend
cd frontend
docker build -t emotional-intelligence-frontend .
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use TypeScript for frontend components
- Write tests for new features
- Update documentation as needed

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for GPT-3.5 API
- Google for OAuth 2.0
- React and Flask communities
- Contributors and testers

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/emotional-intelligence-mood-tracker/issues)
- **Documentation**: [Wiki](https://github.com/yourusername/emotional-intelligence-mood-tracker/wiki)
- **Email**: aditigarg1312@gmail.com

## 🗺️ Roadmap

- [ ] Mobile app development
- [ ] Advanced analytics and ML
- [ ] Social features and sharing
- [ ] Export/import functionality
- [ ] Multi-language support
- [ ] Real-time notifications
- [ ] Integration with health apps

---

**Made with ❤️ for better emotional well-being**

