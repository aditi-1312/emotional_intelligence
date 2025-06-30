import pandas as pd
import numpy as np
import joblib
import re
import nltk
import ssl
import os
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import Dict, List, Tuple, Optional
import logging
from datetime import datetime
from nltk.tokenize import word_tokenize

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fix NLTK SSL issues on macOS
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

class EmotionDataProcessor:
    """
    Enhanced emotion data processor using ensemble models for better accuracy.
    """
    
    def __init__(self, models_dir: str, data_dir: str):
        """
        Initialize the emotion data processor.
        
        Args:
            models_dir: Path to the directory containing trained models
            data_dir: Path to the directory containing data files
        """
        self.models_dir = models_dir
        self.data_dir = data_dir
        self.ensemble_detector = None
        
        # Initialize emotion labels
        self.emotion_labels = ['anger', 'fear', 'joy', 'love', 'neutral', 'sadness', 'surprise']
        
        # Initialize models and vectorizer
        self.models = {}
        self.vectorizer = None
        
        # Initialize NLTK components
        self._initialize_nltk()
        
        # Load models and vectorizer
        self._load_models()
        
        # Load ensemble detector
        self._load_ensemble_detector()
    
    def _initialize_nltk(self):
        """Initialize NLTK components for text processing."""
        try:
            # Download required NLTK data
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('wordnet', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)
            
            self.lemmatizer = WordNetLemmatizer()
            self.stop_words = set(stopwords.words('english'))
            
            logger.info("NLTK components initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing NLTK: {e}")
    
    def _load_models(self):
        """Load all trained models and vectorizer."""
        try:
            # Import config to get model filenames
            from config import Config
            
            # Get model filenames from config
            model_files = Config.MODEL_FILES
            
            # Log which model files we're loading
            logger.info(f"Loading models from config: {model_files}")
            
            # Load TF-IDF vectorizer
            vectorizer_path = os.path.join(self.models_dir, model_files['vectorizer'])
            self.vectorizer = joblib.load(vectorizer_path)
            logger.info(f"TF-IDF vectorizer loaded successfully from: {model_files['vectorizer']}")
            
            # Load all models
            model_names = {
                'decision_tree': 'decision_tree',
                'gradient_boosting': 'gradient_boosting',
                'knn': 'knn',
                'linear_svc': 'linear_svc',
                'logistic_regression': 'logistic_regression',
                'naive_bayes': 'naive_bayes',
                'random_forest': 'random_forest'
            }
            
            for model_name, config_key in model_names.items():
                model_path = os.path.join(self.models_dir, model_files[config_key])
                if os.path.exists(model_path):
                    self.models[model_name] = joblib.load(model_path)
                    logger.info(f"{model_name} model loaded successfully from: {model_files[config_key]}")
                else:
                    logger.warning(f"Model file not found: {model_path}")
                    
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            raise
    
    def _load_ensemble_detector(self):
        """Load the ensemble emotion detector."""
        # Ensemble functionality is now implemented directly in the data processor
        # No need for separate ensemble detector
        pass
    
    def preprocess_text(self, text: str) -> str:
        """
        Preprocess text for emotion analysis.
        
        Args:
            text: Raw text input
            
        Returns:
            Preprocessed text
        """
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep apostrophes
        text = re.sub(r'[^a-zA-Z\s\']', ' ', text)
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stopwords and lemmatize
        processed_tokens = []
        for token in tokens:
            if token not in self.stop_words and len(token) > 2:
                lemmatized = self.lemmatizer.lemmatize(token)
                processed_tokens.append(lemmatized)
        
        return ' '.join(processed_tokens)
    
    def analyze_emotion(self, text: str, model_name: str = 'ensemble') -> Dict:
        """
        Analyze emotion in text using specified model or ensemble.
        
        Args:
            text: Text to analyze
            model_name: Model to use ('ensemble', 'linear_svc', 'logistic_regression', etc.)
            
        Returns:
            Dictionary with emotion analysis results
        """
        try:
            if model_name == 'ensemble':
                return self._analyze_emotion_ensemble(text)
            else:
                return self._analyze_emotion_single_model(text, model_name)
        except Exception as e:
            logger.error(f"Error analyzing emotion: {e}")
            return {
                'emotion': 'neutral',
                'confidence': 0.0,
                'emotions': {emotion: 0.0 for emotion in self.emotion_labels}
            }
    
    def _analyze_emotion_ensemble(self, text: str) -> Dict:
        """
        Analyze emotion using ensemble of all models.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with ensemble analysis results
        """
        # Model weights based on performance
        model_weights = {
            'linear_svc': 0.25,
            'logistic_regression': 0.20,
            'gradient_boosting': 0.20,
            'random_forest': 0.15,
            'naive_bayes': 0.10,
            'knn': 0.05,
            'decision_tree': 0.05
        }
        
        # Get predictions from all models
        predictions = {}
        emotion_scores = {emotion: 0.0 for emotion in self.emotion_labels}
        total_weight = 0.0
        
        for model_name in model_weights.keys():
            try:
                result = self._analyze_emotion_single_model(text, model_name)
                predictions[model_name] = result
                
                weight = model_weights[model_name]
                total_weight += weight
                
                # Add weighted score for predicted emotion
                emotion_scores[result['emotion']] += weight
                
            except Exception as e:
                logger.error(f"Error with {model_name}: {e}")
        
        # Normalize scores
        if total_weight > 0:
            for emotion in emotion_scores:
                emotion_scores[emotion] /= total_weight
        
        # Get ensemble prediction
        dominant_emotion = max(emotion_scores.items(), key=lambda x: x[1])[0]
        confidence = emotion_scores[dominant_emotion]
        
        # Calculate model agreement
        pred_list = [pred['emotion'] for pred in predictions.values()]
        agreement = pred_list.count(dominant_emotion) / len(pred_list) if pred_list else 0.0
        
        return {
            'emotion': dominant_emotion,
            'confidence': confidence,
            'emotions': emotion_scores,
            'model_agreement': agreement,
            'models_used': list(predictions.keys()),
            'ensemble': True,
            'individual_predictions': predictions
        }
    
    def _analyze_emotion_single_model(self, text: str, model_name: str) -> Dict:
        """
        Analyze emotion using a single model.
        
        Args:
            text: Text to analyze
            model_name: Name of the model to use
            
        Returns:
            Dictionary with emotion analysis results
        """
        if not self.vectorizer:
            raise ValueError("Vectorizer not loaded")
        
        # Vectorize text
        X = self.vectorizer.transform([text])
        
        # Get model
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not found")
        
        model = self.models[model_name]
        
        # Get prediction
        prediction = model.predict(X)[0]
        
        # Try to get probabilities
        try:
            probabilities = model.predict_proba(X)[0]
            confidence = max(probabilities)
            emotions = dict(zip(self.emotion_labels, probabilities))
        except:
            # If predict_proba is not available
            confidence = 0.8
            emotions = {emotion: 0.1 if emotion == prediction else 0.0 
                       for emotion in self.emotion_labels}
            emotions[prediction] = confidence
        
        return {
            'emotion': prediction,
            'confidence': confidence,
            'emotions': emotions,
            'model_used': model_name,
            'ensemble': False
        }
    
    def get_detailed_analysis(self, text: str) -> Dict:
        """
        Get detailed emotion analysis with model comparison.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with detailed analysis
        """
        if not self.ensemble_detector:
            return {'error': 'Ensemble detector not available'}
        
        try:
            return self.ensemble_detector.get_all_model_predictions(text)
        except Exception as e:
            logger.error(f"Error in detailed analysis: {e}")
            return {'error': str(e)}
    
    def get_model_performance_analysis(self, text: str) -> Dict:
        """
        Get model performance analysis for the given text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with performance analysis
        """
        if not self.ensemble_detector:
            return {'error': 'Ensemble detector not available'}
        
        try:
            return self.ensemble_detector.get_model_confidence_analysis(text)
        except Exception as e:
            logger.error(f"Error in performance analysis: {e}")
            return {'error': str(e)}
    
    def get_recommended_model_for_text(self, text: str) -> str:
        """
        Get the recommended model for the given text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Name of the recommended model
        """
        if not self.ensemble_detector:
            return 'linear_svc'  # Default fallback
        
        try:
            return self.ensemble_detector.get_recommended_model(text)
        except Exception as e:
            logger.error(f"Error getting recommended model: {e}")
            return 'linear_svc'
    
    def get_emotion_distribution(self, texts: List[str]) -> Dict[str, int]:
        """
        Get emotion distribution from a list of texts.
        
        Args:
            texts: List of texts to analyze
            
        Returns:
            Dictionary with emotion counts
        """
        emotion_counts = {emotion: 0 for emotion in self.emotion_labels}
        
        for text in texts:
            if text:
                analysis = self.analyze_emotion(text)
                emotion = analysis.get('dominant_emotion', analysis.get('emotion', 'neutral'))
                if emotion in emotion_counts:
                    emotion_counts[emotion] += 1
        
        return emotion_counts
    
    def get_sentiment_score(self, text: str) -> float:
        """
        Get sentiment score using TextBlob.
        
        Args:
            text: Input text
            
        Returns:
            Sentiment polarity score (-1 to 1)
        """
        try:
            blob = TextBlob(text)
            return float(blob.sentiment.polarity)
        except Exception as e:
            logger.warning(f"Error getting sentiment score: {e}")
            return 0.0
    
    def load_dataset(self) -> pd.DataFrame:
        """
        Load the emotion dataset.
        
        Returns:
            DataFrame containing the emotion dataset
        """
        try:
            dataset_path = f"{self.data_dir}/emotion_dataset.csv"
            df = pd.read_csv(dataset_path)
            logger.info(f"Dataset loaded successfully: {len(df)} entries")
            return df
        except Exception as e:
            logger.error(f"Error loading dataset: {e}")
            return pd.DataFrame()
    
    def get_emotion_statistics(self, texts: List[str]) -> Dict:
        """
        Get comprehensive emotion statistics from a list of texts.
        
        Args:
            texts: List of texts to analyze
            
        Returns:
            Dictionary with emotion statistics
        """
        if not texts:
            return {
                'total_entries': 0,
                'emotion_distribution': {},
                'average_confidence': 0.0,
                'most_common_emotion': 'neutral',
                'sentiment_distribution': {'positive': 0, 'neutral': 0, 'negative': 0}
            }
        
        emotion_counts = {emotion: 0 for emotion in self.emotion_labels}
        confidences = []
        sentiments = []
        
        for text in texts:
            if text:
                # Emotion analysis
                analysis = self.analyze_emotion(text)
                emotion = analysis.get('dominant_emotion', analysis.get('emotion', 'neutral'))
                if emotion in emotion_counts:
                    emotion_counts[emotion] += 1
                confidences.append(analysis.get('confidence', 0.0))
                
                # Sentiment analysis
                sentiment = self.get_sentiment_score(text)
                sentiments.append(sentiment)
        
        # Calculate statistics
        total_entries = len([t for t in texts if t])
        average_confidence = np.mean(confidences) if confidences else 0.0
        most_common_emotion = max(emotion_counts.items(), key=lambda x: x[1])[0]
        
        # Sentiment distribution
        sentiment_dist = {'positive': 0, 'neutral': 0, 'negative': 0}
        for sentiment in sentiments:
            if sentiment > 0.1:
                sentiment_dist['positive'] += 1
            elif sentiment < -0.1:
                sentiment_dist['negative'] += 1
            else:
                sentiment_dist['neutral'] += 1
        
        return {
            'total_entries': total_entries,
            'emotion_distribution': emotion_counts,
            'average_confidence': float(average_confidence),
            'most_common_emotion': most_common_emotion,
            'sentiment_distribution': sentiment_dist,
            'average_sentiment': float(np.mean(sentiments)) if sentiments else 0.0
        } 