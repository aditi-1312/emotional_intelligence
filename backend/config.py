"""
Configuration file for Emotional Intelligence Project
Contains all settings and parameters for the system
"""

import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"
MODELS_DIR = PROJECT_ROOT / "models"
LOGS_DIR = PROJECT_ROOT / "logs"

# Create directories if they don't exist
for directory in [DATA_DIR, OUTPUT_DIR, MODELS_DIR, LOGS_DIR]:
    directory.mkdir(exist_ok=True)

# Data configuration
DATA_CONFIG = {
    "dataset_path": DATA_DIR / "emotion_dataset.csv",  # Path to our downloaded dataset
    "sample_size": 2000,
    "test_size": 0.2,
    "random_state": 42,
    "text_column": "text",
    "label_column": "label",
    "emotion_mapping": {
        "sadness": "sadness",
        "joy": "joy", 
        "love": "love",
        "anger": "anger",
        "fear": "fear",
        "surprise": "surprise",
        "neutral": "neutral"
    }
}

# Text processing configuration
TEXT_PROCESSING_CONFIG = {
    "use_lemmatization": True,
    "use_stemming": False,
    "remove_stopwords": True,
    "min_word_length": 3,
    "max_word_length": 20,
    "custom_stop_words": [
        "really", "very", "quite", "extremely", "totally", "completely",
        "absolutely", "definitely", "certainly", "surely", "obviously"
    ]
}

# Feature extraction configuration
FEATURE_EXTRACTION_CONFIG = {
    "tfidf_max_features": 5000,
    "tfidf_ngram_range": (1, 2),
    "count_max_features": 2500,
    "count_ngram_range": (1, 1),
    "min_df": 2,
    "max_df": 0.95
}

# Model configuration
MODEL_CONFIG = {
    "models_to_train": [
        "logistic_regression",
        "linear_svc", 
        "random_forest",
        "gradient_boosting",
        "naive_bayes"
    ],
    "hyperparameters": {
        "logistic_regression": {
            "max_iter": 1000,
            "solver": "liblinear",
            "C": 1.0
        },
        "linear_svc": {
            "max_iter": 1000,
            "C": 1.0
        },
        "random_forest": {
            "n_estimators": 100,
            "max_depth": 10,
            "random_state": 42
        },
        "gradient_boosting": {
            "n_estimators": 100,
            "learning_rate": 0.1,
            "max_depth": 3,
            "random_state": 42
        },
        "naive_bayes": {
            "alpha": 1.0
        }
    }
}

# API configuration
API_CONFIG = {
    "host": "0.0.0.0",
    "port": 5000,
    "debug": True,
    "max_batch_size": 100,
    "rate_limit": 100,  # requests per minute
    "timeout": 30  # seconds
}

# Streamlit configuration
STREAMLIT_CONFIG = {
    "page_title": "Emotional Intelligence Analyzer",
    "page_icon": "🧠",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Visualization configuration
VISUALIZATION_CONFIG = {
    "default_figure_size": (800, 600),
    "color_palette": "viridis",
    "theme": "plotly_white",
    "export_formats": ["png", "html", "json"]
}

# Logging configuration
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": LOGS_DIR / "app.log",
    "max_file_size": 10 * 1024 * 1024,  # 10MB
    "backup_count": 5
}

# Emotion keywords for analysis
EMOTION_KEYWORDS = {
    "joy": [
        "happy", "joy", "excited", "thrilled", "delighted", "pleased", 
        "great", "wonderful", "fantastic", "amazing", "brilliant", "excellent"
    ],
    "sadness": [
        "sad", "depressed", "melancholy", "gloomy", "miserable", "sorrowful",
        "unhappy", "down", "blue", "disappointed", "upset", "heartbroken"
    ],
    "anger": [
        "angry", "furious", "irritated", "annoyed", "mad", "rage", "frustrated",
        "outraged", "livid", "enraged", "irate", "incensed"
    ],
    "fear": [
        "afraid", "scared", "terrified", "anxious", "worried", "fearful",
        "nervous", "panicked", "horrified", "dread", "alarmed", "frightened"
    ],
    "surprise": [
        "surprised", "shocked", "amazed", "astonished", "stunned", "wow",
        "incredible", "unbelievable", "remarkable", "extraordinary", "unexpected"
    ],
    "love": [
        "love", "adore", "cherish", "affection", "romantic", "passionate",
        "fond", "devoted", "tender", "caring", "warm", "loving"
    ]
}

# Performance thresholds
PERFORMANCE_THRESHOLDS = {
    "excellent_accuracy": 0.85,
    "good_accuracy": 0.75,
    "acceptable_accuracy": 0.65,
    "min_confidence": 0.5,
    "max_training_time": 300,  # seconds
    "max_prediction_time": 5   # seconds
}

# File paths
FILE_PATHS = {
    "emotions_dataset": DATA_DIR / "emotion_dataset.csv",  # Our downloaded dataset
    "sample_data": DATA_DIR / "emotion_dataset.csv",
    "best_model": OUTPUT_DIR / "best_model.pkl",
    "feature_extractor": OUTPUT_DIR / "feature_extractor.pkl",
    "text_processor": OUTPUT_DIR / "text_processor.pkl",
    "training_results": OUTPUT_DIR / "training_results.json",
    "analysis_report": OUTPUT_DIR / "analysis_report.html"
}

# Environment variables
ENV_VARS = {
    "FLASK_ENV": os.getenv("FLASK_ENV", "development"),
    "DEBUG": os.getenv("DEBUG", "True").lower() == "true",
    "PORT": int(os.getenv("PORT", 5000)),
    "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO")
}

# Validation rules
VALIDATION_RULES = {
    "min_text_length": 1,
    "max_text_length": 10000,
    "allowed_emotions": list(EMOTION_KEYWORDS.keys()) + ["neutral"],
    "max_batch_size": 100,
    "supported_languages": ["en"]  # Currently only English
} 