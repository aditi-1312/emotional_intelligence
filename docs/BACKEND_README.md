# 🧠 Emotional Intelligence Backend

A comprehensive Python backend for emotion analysis using machine learning models, built with Flask and Streamlit.

## 🚀 Features

- **Flask API**: RESTful API for emotion analysis and journal management
- **Streamlit Dashboard**: Interactive web interface for data visualization and model testing
- **ML Models**: Multiple scikit-learn models for emotion classification
- **TF-IDF Vectorization**: Advanced text processing for accurate emotion detection
- **Analytics**: Comprehensive emotional insights and pattern analysis
- **Wellness Suggestions**: Personalized recommendations based on emotional state

## 📋 Requirements

- Python 3.9+
- All dependencies listed in `requirements.txt`

## 🛠️ Installation

1. **Clone the repository** (if not already done):
   ```bash
   cd emotional_intelligence/backend
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**:
   ```bash
   python -c "import flask, streamlit, pandas, numpy, sklearn; print('✅ All dependencies installed!')"
   ```

## 🚀 Quick Start

### Option 1: Flask API Only
```bash
python run_api.py
```
The API will be available at `http://localhost:5001`

### Option 2: Streamlit Dashboard Only
```bash
streamlit run run_app.py
```
The dashboard will be available at `http://localhost:8501`

### Option 3: Both (Recommended)
Run in separate terminals:
```bash
# Terminal 1 - API
python run_api.py

# Terminal 2 - Dashboard
streamlit run run_app.py
```

## 📡 API Endpoints

### Health Check
- `GET /health` - Check API status

### Emotion Analysis
- `POST /analyze` - Analyze emotion in text
  ```json
  {
    "text": "I'm feeling happy today!",
    "model": "logistic_regression"
  }
  ```

### Journal Management
- `GET /journal` - Get journal entries
- `POST /journal` - Add new journal entry
  ```json
  {
    "text": "Today was amazing!",
    "user_id": "user123"
  }
  ```

### Analytics
- `GET /analytics/summary` - Get analytics summary
- `GET /analytics/timeline` - Get timeline data

### Wellness & Insights
- `GET /suggestions` - Get wellness suggestions
- `GET /ai/insights` - Get AI-powered insights

### Model Performance
- `GET /models/performance` - Get model performance metrics

## 🎯 ML Models

The system includes multiple trained models:
- **Logistic Regression** (default)
- **Random Forest**
- **Gradient Boosting**
- **Linear SVC**
- **Naive Bayes**
- **K-Nearest Neighbors**
- **Decision Tree**

## 📊 Supported Emotions

The system can detect 7 emotions:
- 😊 **Joy** - Happiness, excitement, delight
- 😢 **Sadness** - Sorrow, disappointment, melancholy
- 😠 **Anger** - Frustration, irritation, rage
- 😨 **Fear** - Anxiety, worry, terror
- 😍 **Love** - Affection, adoration, fondness
- 😲 **Surprise** - Astonishment, amazement, shock
- 😐 **Neutral** - Balanced, calm, indifferent

## 🔧 Configuration

### Environment Variables
- `FLASK_DEBUG` - Enable/disable debug mode (default: True)
- `PORT` - API port (default: 5001)
- `HOST` - API host (default: 0.0.0.0)
- `SECRET_KEY` - Flask secret key (for production)

### File Structure
```
backend/
├── api.py              # Flask API server
├── config.py           # Configuration settings
├── data_processor.py   # Text processing and ML
├── models.py           # Model management
├── run_api.py          # API runner script
├── run_app.py          # Streamlit dashboard
├── requirements.txt    # Python dependencies
├── Procfile           # Heroku deployment
└── runtime.txt        # Python version
```

## 📈 Usage Examples

### Python API Client
```python
import requests

# Analyze emotion
response = requests.post('http://localhost:5001/analyze', json={
    'text': 'I feel amazing today!',
    'model': 'logistic_regression'
})
print(response.json())

# Add journal entry
response = requests.post('http://localhost:5001/journal', json={
    'text': 'Today was productive and fulfilling.',
    'user_id': 'user123'
})
print(response.json())
```

### cURL Examples
```bash
# Health check
curl http://localhost:5001/health

# Analyze emotion
curl -X POST http://localhost:5001/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "I am so happy!", "model": "logistic_regression"}'

# Get analytics
curl http://localhost:5001/analytics/summary
```

## 🚀 Deployment

### Heroku
1. Create a Heroku app
2. Set environment variables
3. Deploy using Git:
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

### Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5001
CMD ["gunicorn", "api:app"]
```

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**:
   ```bash
   # Find process using port 5001
   lsof -i :5001
   # Kill process
   kill -9 <PID>
   ```

2. **Model loading errors**:
   - Ensure `data_and_models/models/` contains the `.pkl` files
   - Check file permissions

3. **NLTK data missing**:
   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('stopwords')
   nltk.download('wordnet')
   ```

### Debug Mode
Set `FLASK_DEBUG=True` for detailed error messages and auto-reload.

## 📝 Development

### Adding New Models
1. Train model using scikit-learn
2. Save as `.pkl` file in `data_and_models/models/`
3. Update `config.py` with model filename
4. Add model to `data_processor.py`

### Extending API
1. Add new endpoints in `api.py`
2. Update documentation
3. Add tests (recommended)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Scikit-learn for ML capabilities
- Flask for the web framework
- Streamlit for the dashboard
- NLTK for text processing
- Plotly for visualizations

---

**Happy Emotion Analysis! 🧠✨** 