# 🧠 Emotional Intelligence Analyzer

A comprehensive web application for analyzing emotional intelligence using AI-powered emotion analysis and interactive visualizations.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.25+-green.svg)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Features

### 📝 **Text Analysis**
- Analyze emotions from natural language text
- AI-powered emotion detection with confidence scoring
- Real-time emotion analysis with multiple ML models
- Support for 7 emotion categories: joy, sadness, anger, fear, surprise, love, neutral

### 📊 **Interactive Dashboard**
- Real-time emotion analysis results
- Interactive visualizations with Plotly
- Emotion distribution charts and radar plots
- Sentiment analysis with gauge charts

### 📈 **Model Training Interface**
- Train multiple ML models (Logistic Regression, Random Forest, SVM, etc.)
- Model performance comparison
- Hyperparameter tuning capabilities
- Model evaluation and selection

### 📋 **Data Explorer**
- Sample dataset exploration
- Emotion distribution analysis
- Text length statistics
- Interactive data visualizations

### 🤖 **Advanced ML Models**
- Multiple emotion classification models
- Feature extraction with TF-IDF
- Text preprocessing and cleaning
- Model performance metrics

### 🎨 **Beautiful UI**
- Modern Streamlit interface
- Responsive design
- Interactive charts and graphs
- Custom CSS styling

## 🛠️ Technology Stack

### **Backend & ML**
- **Python 3.8+** - Core programming language
- **Streamlit** - Web application framework
- **Scikit-learn** - Machine learning library
- **Pandas/NumPy** - Data processing
- **NLTK/TextBlob** - Natural language processing
- **Plotly** - Interactive visualizations
- **SQLite** - Local data storage

### **Machine Learning**
- **Multiple ML Models** - Logistic Regression, Random Forest, SVM, Naive Bayes
- **Feature Extraction** - TF-IDF, Count Vectorization
- **Text Processing** - Lemmatization, stop word removal
- **Model Evaluation** - Cross-validation, performance metrics

### **DevOps**
- **Docker** - Containerization
- **Git** - Version control
- **Python venv** - Environment management

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/emotional-intelligence-analyzer.git
cd emotional-intelligence-analyzer
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Train Models (Optional)
```bash
# Train the emotion analysis models
python train_models.py
```

### 4. Run the Application
```bash
# Method 1: Using the launch script
python run_app.py

# Method 2: Direct Streamlit command
streamlit run app.py

# Method 3: With custom port
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

### 5. Access the Application
- Web Interface: http://localhost:8501
- The application will automatically open in your default browser

## 📁 Project Structure

```
emotional-intelligence-analyzer/
├── backend/                 # Main application directory
│   ├── app.py              # Streamlit application
│   ├── run_app.py          # Launch script
│   ├── config.py           # Configuration management
│   ├── models.py           # Data models and database
│   ├── train_models.py     # Model training script
│   ├── requirements.txt    # Python dependencies
│   ├── Procfile           # Deployment configuration
│   └── src/
│       ├── data_processor.py  # Text processing
│       ├── models.py          # ML models
│       └── utils.py           # Utility functions
├── data_and_models/        # Data storage and trained models
├── docs/                   # Documentation
├── scripts/                # Utility scripts
├── temp_cleanup/           # Legacy files
├── frontend/               # React frontend (legacy)
└── README.md              # This file
```

## 🔧 Configuration

### Environment Variables
The application uses default configurations, but you can customize:

```bash
# Set custom port
export PORT=8501

# Enable debug mode
export DEBUG=True

# Set log level
export LOG_LEVEL=INFO
```

### Model Configuration
Edit `backend/config.py` to customize:
- Model hyperparameters
- Text processing settings
- Feature extraction parameters
- Performance thresholds

## 🧪 Testing

### Run System Tests
```bash
cd backend
python ../scripts/test_system.py
```

### Run Demo
```bash
cd backend
python ../scripts/run_demo.py
```

## 🚀 Deployment

### Local Development
```bash
cd backend
streamlit run app.py
```

### Production Deployment
```bash
# Using the Procfile (for Heroku, Railway, etc.)
cd backend
# The Procfile will automatically run: streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

### Docker Deployment
```bash
# Build and run with Docker
docker build -t emotional-intelligence .
docker run -p 8501:8501 emotional-intelligence
```

## 📊 Features in Detail

### Text Analysis
- **Real-time Processing**: Analyze text as you type
- **Multiple Emotions**: Detect joy, sadness, anger, fear, surprise, love, neutral
- **Confidence Scoring**: Get confidence levels for each emotion
- **Sentiment Analysis**: Overall sentiment scoring

### Dashboard
- **Overview Metrics**: Total analyses, accuracy, common emotions
- **Quick Analysis**: Instant text analysis with results
- **Activity Tracking**: Daily analysis trends
- **Performance Monitoring**: Model performance metrics

### Model Training
- **Multiple Algorithms**: Logistic Regression, Random Forest, SVM, Naive Bayes
- **Hyperparameter Tuning**: Optimized model parameters
- **Performance Comparison**: Side-by-side model evaluation
- **Model Persistence**: Save and load trained models

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Streamlit for the amazing web framework
- Scikit-learn for machine learning capabilities
- Plotly for interactive visualizations
- The open-source community for inspiration and tools

