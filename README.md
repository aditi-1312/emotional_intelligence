# 🧠 Emotional Intelligence Mood Tracker

A comprehensive mood tracking and emotional intelligence application with a React frontend and Flask backend. This project provides advanced text emotion analysis, daily journaling, mood analytics, and personalized insights powered by AI.

## 📁 Project Structure

```
emotional_intelligence/
├── 📄 README.md                    # Main project documentation
├── 📄 LICENSE                      # MIT License
├── 📄 requirements.txt             # Python dependencies
├── 📄 config.env.example           # Environment configuration template
├── 📄 .gitignore                   # Git ignore patterns
├── 📄 docker-compose.yml           # Docker configuration
├── 📄 Dockerfile                   # Docker image definition
│
├── 🔧 Backend/
│   ├── api.py                      # Flask REST API
│   ├── models.py                   # ML models and emotion analysis
│   ├── config.py                   # Configuration settings
│   └── src/                        # Source code modules
│       ├── __init__.py
│       ├── data_processor.py       # Text processing
│       ├── models.py               # ML models
│       └── utils.py                # Utility functions
│
├── 🎨 Frontend/
│   ├── package.json                # Node.js dependencies
│   ├── public/                     # Static assets
│   └── src/                        # React source code
│       ├── components/             # React components
│       │   ├── JournalEntry.tsx    # Journal entry component
│       │   ├── Dashboard.tsx       # Analytics dashboard
│       │   ├── Timeline.tsx        # Timeline view
│       │   ├── MoodCalendar.tsx    # Calendar view
│       │   └── Advice.tsx          # AI insights
│       ├── services/               # API service layer
│       └── App.tsx                 # Main application
│
├── 📚 Documentation/
│   ├── DEPLOYMENT.md               # Deployment instructions
│   ├── GITHUB_DEPLOYMENT.md        # GitHub deployment guide
│   ├── CONTRIBUTING.md             # Contributing guidelines
│   ├── CHANGELOG.md                # Version history
│   ├── SETUP.md                    # Setup instructions
│   ├── CHATGPT_SETUP.md            # ChatGPT integration guide
│   └── ENHANCEMENT_SUMMARY.md      # Project enhancement summary
│
├── 🔧 Scripts/
│   ├── deploy.sh                   # Deployment script
│   ├── run_demo.py                 # Demo runner
│   ├── test_system.py              # System testing
│   └── system_status.py            # System status checker
│
├── 📊 Data & Models/
│   ├── data/                       # Data storage
│   ├── models/                     # Trained ML models
│   └── output/                     # Generated outputs
│
├── 🧪 Examples/
│   └── emotional_intellegence-1.ipynb  # Jupyter notebook example
│
├── 🧪 Tests/
│   └── (Test files will be added here)
│
└── 🚀 CI/CD/
    └── .github/workflows/          # GitHub Actions
        └── deploy.yml              # CI/CD pipeline
```

## ✨ Features

### 🎯 Core Capabilities
- **Daily Mood Journaling**: Track your emotions through daily journal entries
- **AI-Powered Emotion Analysis**: Advanced text emotion classification using machine learning
- **Mood Analytics Dashboard**: Visualize your emotional patterns and trends
- **Personalized Insights**: AI-generated advice based on your mood patterns
- **Mood Calendar**: Calendar view of your daily moods with color coding
- **Timeline Analysis**: Track your emotional journey over time
- **Daily Quotes**: Motivational quotes that adapt to your mood

### 🤖 Machine Learning Models
- **Multi-Model Ensemble**: Support for 7+ machine learning models
- **Advanced Text Processing**: Lemmatization, stemming, custom stop words
- **Real-time Analysis**: Instant emotion detection and sentiment analysis
- **Context-Aware Detection**: Improved accuracy for positive vs negative emotions

### 📊 Analytics & Visualization
- **Mood Distribution Charts**: Interactive pie charts and bar plots
- **Emotion Timeline**: Track emotions over time with detailed entries
- **Monthly Mood Statistics**: Comprehensive mood analytics
- **Personalized Insights**: AI-powered recommendations and advice
- **Mood Calendar**: Visual calendar with color-coded daily moods

### 🌐 Web Interfaces
- **React Frontend**: Modern, responsive web application
- **Flask REST API**: Production-ready API endpoints
- **Real-time Updates**: Live dashboard updates
- **Mobile-Friendly Design**: Responsive design for all devices

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/aditi-1312/emotional_intelligence.git
cd emotional_intelligence

# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install
cd ..
```

### 2. Configuration

```bash
# Copy and edit environment configuration
cp config.env.example config.env
# Edit config.env with your API keys and settings
```

### 3. Start the Application

#### Option A: Using the deployment script
```bash
# Setup and start development servers
./scripts/deploy.sh setup
./scripts/deploy.sh dev
```

#### Option B: Manual startup
```bash
# Start the Flask API server
PORT=5001 python3 api.py

# In another terminal, start the React development server
cd frontend
npm start
```

The web application will be available at `http://localhost:3000`

## 📚 Documentation

- **[Setup Guide](docs/SETUP.md)** - Detailed setup instructions
- **[Deployment Guide](docs/DEPLOYMENT.md)** - Production deployment
- **[GitHub Deployment](docs/GITHUB_DEPLOYMENT.md)** - GitHub-specific deployment
- **[Contributing Guidelines](docs/CONTRIBUTING.md)** - How to contribute
- **[Changelog](docs/CHANGELOG.md)** - Version history and updates
- **[ChatGPT Setup](docs/CHATGPT_SETUP.md)** - AI integration guide

## 🎮 Usage

### Web Application Features

1. **Journal Entry**: Write daily journal entries and get instant emotion analysis
2. **Dashboard**: View mood analytics, current mood, and daily quotes
3. **Timeline**: Browse your journal entries chronologically
4. **Mood Calendar**: Visual calendar showing your daily moods
5. **Advice**: Get personalized insights and AI-powered recommendations

### API Endpoints

#### Journal Management
```bash
# Create a new journal entry
curl -X POST http://localhost:5001/journal \
  -H "Content-Type: application/json" \
  -d '{"text": "I am feeling really happy today!", "user_id": "user123"}'

# Get journal entries
curl http://localhost:5001/journal?user_id=user123&limit=10
```

#### Analytics
```bash
# Get mood analytics summary
curl http://localhost:5001/analytics/summary?user_id=user123

# Get mood timeline
curl http://localhost:5001/analytics/timeline?user_id=user123
```

#### AI Insights
```bash
# Get personalized AI insights
curl -X POST http://localhost:5001/ai/insights \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123"}'
```

## 📊 Supported Emotions

The system can detect and classify the following emotions:

- **Joy** 😊: Happiness, excitement, delight
- **Sadness** 😢: Depression, melancholy, sorrow
- **Anger** 😠: Fury, irritation, rage
- **Fear** 😨: Anxiety, terror, worry
- **Surprise** 😲: Shock, amazement, astonishment
- **Love** ❤️: Affection, adoration, passion
- **Neutral** 😐: Balanced, indifferent, calm

## 🎯 Features

### Daily Journaling
- **Emotion Detection**: Automatic emotion analysis of your journal entries
- **Mood Tracking**: Track your daily emotional state
- **Rich Text Support**: Support for detailed journal entries
- **Instant Analysis**: Real-time emotion classification

### Analytics Dashboard
- **Mood Distribution**: Visual breakdown of your emotions
- **Current Mood Display**: Shows your most recent emotional state
- **Daily Quotes**: Motivational quotes that adapt to your mood
- **Trend Analysis**: Track emotional patterns over time

### Mood Calendar
- **Visual Calendar**: Monthly view of your moods
- **Color Coding**: Each emotion has a distinct color
- **Day Details**: Click on any day to see journal entries
- **Monthly Statistics**: Summary of your monthly emotional patterns

### AI-Powered Insights
- **Personalized Advice**: AI-generated recommendations based on your patterns
- **Mood Analysis**: Deep insights into your emotional journey
- **Professional Resources**: Mental health resources and tips
- **ChatGPT Integration**: Advanced AI insights with fallback to rule-based advice

### Timeline View
- **Chronological View**: Browse all your journal entries
- **Emotion Filtering**: Filter entries by emotion
- **Search Functionality**: Find specific entries
- **Detailed View**: Full journal entry display

## 🔧 Configuration

### Environment Variables
Create a `config.env` file with the following variables:

```env
OPENAI_API_KEY=your_openai_api_key_here
FLASK_SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///instance/emotional_intelligence.db
```

### API Configuration
The API is configured through `config.py`:
- **Server Settings**: Port and host configuration
- **Model Parameters**: ML model settings
- **Database Settings**: SQLite database configuration
- **CORS Settings**: Cross-origin resource sharing

## 🚀 Deployment

### Local Development
```bash
# Backend
PORT=5001 python3 api.py

# Frontend
cd frontend
npm start
```

### Production Deployment
```bash
# Build frontend for production
cd frontend
npm run build

# Deploy backend with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 api:app
```

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up --build
```

## 📈 Performance

- **Emotion Detection Accuracy**: 85-90%
- **Response Time**: <1 second per analysis
- **Real-time Updates**: Instant dashboard refresh
- **Scalable Architecture**: Ready for production deployment

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](docs/CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Dataset**: Emotion Dataset for Emotion Recognition Tasks (Kaggle)
- **Libraries**: React, Flask, scikit-learn, NLTK, OpenAI
- **Community**: Open source contributors and researchers

## 📞 Support

- **Issues**: Report bugs and request features on [GitHub Issues](https://github.com/aditi-1312/emotional_intelligence/issues)
- **Documentation**: Comprehensive setup guides in the `/docs` folder
- **Examples**: Sample usage in the `/examples` folder

## 🔮 Future Enhancements

- **Multi-language Support**: Expand beyond English
- **Voice Analysis**: Audio emotion detection
- **Mobile App**: Native mobile application
- **Social Features**: Share insights with friends
- **Advanced Analytics**: Machine learning insights
- **Integration**: Connect with other health apps

---

**Made with ❤️ for emotional intelligence and mental wellness**

