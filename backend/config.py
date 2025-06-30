import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent

# Data and models paths
DATA_DIR = BASE_DIR / "data_and_models" / "data"
MODELS_DIR = BASE_DIR / "data_and_models" / "models"
WELLNESS_FILE = BASE_DIR / "wellness_suggestions.json"

# Flask configuration
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    PORT = int(os.environ.get('PORT', 5001))
    HOST = os.environ.get('HOST', '0.0.0.0')
    
    # CORS settings
    CORS_ORIGINS = [
        'http://localhost:3000',
        'http://127.0.0.1:3000',
        'http://localhost:8501',
        'http://127.0.0.1:8501'
    ]
    
    # ML Model settings
    MODEL_FILES = {
        'vectorizer': 'vectorizer_20250630_014526.pkl',
        'best_model': 'best_model_info_20250630_014526.pkl',
        'decision_tree': 'decision_tree_20250630_014526.pkl',
        'gradient_boosting': 'gradient_boosting_20250630_014526.pkl',
        'knn': 'knn_20250630_014526.pkl',
        'linear_svc': 'linear_svc_20250630_014526.pkl',
        'logistic_regression': 'logistic_regression_20250630_014526.pkl',
        'naive_bayes': 'naive_bayes_20250630_014526.pkl',
        'random_forest': 'random_forest_20250630_014526.pkl'
    }
    
    # Emotion labels
    EMOTION_LABELS = ['anger', 'fear', 'joy', 'love', 'neutral', 'sadness', 'surprise']
    
    # API settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    JOURNAL_ENTRIES_LIMIT = 1000  # Max journal entries to store in memory
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# Development configuration
class DevelopmentConfig(Config):
    DEBUG = True

# Production configuration
class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')

# Testing configuration
class TestingConfig(Config):
    TESTING = True
    DEBUG = True

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 