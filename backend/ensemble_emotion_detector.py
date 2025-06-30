#!/usr/bin/env python3
"""
Ensemble Emotion Detector
Combines predictions from all trained models for better accuracy and reliability.
"""

import numpy as np
import joblib
import os
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)

class EnsembleEmotionDetector:
    """
    Ensemble emotion detector that combines predictions from multiple models.
    """
    
    def __init__(self, models_dir: str):
        """
        Initialize the ensemble detector with all available models.
        
        Args:
            models_dir: Path to the directory containing trained models
        """
        self.models_dir = models_dir
        self.models = {}
        self.vectorizer = None
        self.emotion_labels = ['anger', 'fear', 'joy', 'love', 'neutral', 'sadness', 'surprise']
        
        # Model weights based on individual performance
        self.model_weights = {
            'linear_svc': 0.25,           # Best performer (93.3%)
            'logistic_regression': 0.20,  # Second best (86.7%)
            'gradient_boosting': 0.20,    # Third best (86.7%)
            'random_forest': 0.15,        # Good performer (73.3%)
            'naive_bayes': 0.10,          # Moderate performer (73.3%)
            'knn': 0.05,                  # Lower performer (60%)
            'decision_tree': 0.05         # Lowest performer (33.3%)
        }
        
        self._load_all_models()
    
    def _load_all_models(self):
        """Load all available models and the vectorizer."""
        try:
            # Import config to get model filenames
            from config import Config
            
            # Get model filenames from config
            model_files = Config.MODEL_FILES
            
            # Log which model files we're loading
            logger.info(f"Loading ensemble models from config: {model_files}")
            
            # Load vectorizer
            vectorizer_path = os.path.join(self.models_dir, model_files['vectorizer'])
            self.vectorizer = joblib.load(vectorizer_path)
            logger.info(f"TF-IDF vectorizer loaded successfully from: {model_files['vectorizer']}")
            
            # Load all models
            model_configs = {
                'decision_tree': 'decision_tree',
                'gradient_boosting': 'gradient_boosting',
                'knn': 'knn',
                'linear_svc': 'linear_svc',
                'logistic_regression': 'logistic_regression',
                'naive_bayes': 'naive_bayes',
                'random_forest': 'random_forest'
            }
            
            for model_name, config_key in model_configs.items():
                model_path = os.path.join(self.models_dir, model_files[config_key])
                if os.path.exists(model_path):
                    self.models[model_name] = joblib.load(model_path)
                    logger.info(f"{model_name} model loaded successfully from: {model_files[config_key]}")
                else:
                    logger.warning(f"Model file not found: {model_path}")
                    
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            raise
    
    def get_individual_predictions(self, text: str) -> Dict[str, Dict]:
        """
        Get predictions from all individual models.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with predictions from each model
        """
        if not self.vectorizer:
            return {}
        
        # Vectorize text
        X = self.vectorizer.transform([text])
        
        predictions = {}
        
        for model_name, model in self.models.items():
            try:
                # Get prediction
                pred = model.predict(X)[0]
                
                # Try to get probabilities
                try:
                    probs = model.predict_proba(X)[0]
                    confidence = max(probs)
                    emotions = dict(zip(self.emotion_labels, probs))
                except:
                    # If predict_proba is not available
                    confidence = 0.8
                    emotions = {emotion: 0.1 if emotion == pred else 0.0 
                               for emotion in self.emotion_labels}
                    emotions[pred] = confidence
                
                predictions[model_name] = {
                    'prediction': pred,
                    'confidence': confidence,
                    'emotions': emotions,
                    'weight': self.model_weights.get(model_name, 0.1)
                }
                
            except Exception as e:
                logger.error(f"Error with {model_name}: {e}")
                predictions[model_name] = {
                    'prediction': 'neutral',
                    'confidence': 0.0,
                    'emotions': {emotion: 0.0 for emotion in self.emotion_labels},
                    'weight': 0.0
                }
        
        return predictions
    
    def get_ensemble_prediction(self, text: str) -> Dict:
        """
        Get ensemble prediction combining all models.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with ensemble prediction results
        """
        individual_predictions = self.get_individual_predictions(text)
        
        if not individual_predictions:
            return {
                'dominant_emotion': 'neutral',
                'confidence': 0.0,
                'emotions': {emotion: 0.0 for emotion in self.emotion_labels},
                'model_agreement': 0.0,
                'individual_predictions': {}
            }
        
        # Calculate weighted emotion scores
        emotion_scores = {emotion: 0.0 for emotion in self.emotion_labels}
        total_weight = 0.0
        
        for model_name, pred_info in individual_predictions.items():
            weight = pred_info['weight']
            total_weight += weight
            
            # Add weighted emotion scores
            for emotion, score in pred_info['emotions'].items():
                emotion_scores[emotion] += score * weight
        
        # Normalize scores
        if total_weight > 0:
            for emotion in emotion_scores:
                emotion_scores[emotion] /= total_weight
        
        # Get dominant emotion
        dominant_emotion = max(emotion_scores.items(), key=lambda x: x[1])[0]
        confidence = emotion_scores[dominant_emotion]
        
        # Calculate model agreement
        predictions = [pred['prediction'] for pred in individual_predictions.values()]
        model_agreement = predictions.count(dominant_emotion) / len(predictions)
        
        return {
            'dominant_emotion': dominant_emotion,
            'confidence': confidence,
            'emotions': emotion_scores,
            'model_agreement': model_agreement,
            'individual_predictions': individual_predictions,
            'models_used': list(individual_predictions.keys())
        }
    
    def get_model_confidence_analysis(self, text: str) -> Dict:
        """
        Get detailed analysis of model confidence and agreement.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with confidence analysis
        """
        ensemble_result = self.get_ensemble_prediction(text)
        individual_predictions = ensemble_result['individual_predictions']
        
        # Analyze confidence distribution
        confidences = [pred['confidence'] for pred in individual_predictions.values()]
        avg_confidence = np.mean(confidences) if confidences else 0.0
        std_confidence = np.std(confidences) if len(confidences) > 1 else 0.0
        
        # Find most confident model
        most_confident_model = max(individual_predictions.items(), 
                                 key=lambda x: x[1]['confidence'])[0]
        
        # Count predictions for each emotion
        emotion_counts = {}
        for pred_info in individual_predictions.values():
            emotion = pred_info['prediction']
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        return {
            'ensemble_result': ensemble_result,
            'confidence_analysis': {
                'average_confidence': avg_confidence,
                'confidence_std': std_confidence,
                'most_confident_model': most_confident_model,
                'model_agreement': ensemble_result['model_agreement'],
                'emotion_distribution': emotion_counts
            }
        }
    
    def get_recommended_model(self, text: str) -> str:
        """
        Get the recommended model based on text characteristics.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Name of the recommended model
        """
        # Simple heuristic: use different models for different text lengths
        text_length = len(text.split())
        
        if text_length < 5:
            return 'linear_svc'  # Good for short texts
        elif text_length < 15:
            return 'logistic_regression'  # Balanced for medium texts
        else:
            return 'gradient_boosting'  # Good for longer texts
    
    def get_all_model_predictions(self, text: str) -> Dict:
        """
        Get predictions from all models with detailed comparison.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with all model predictions and comparison
        """
        individual_predictions = self.get_individual_predictions(text)
        ensemble_result = self.get_ensemble_prediction(text)
        
        # Create comparison table
        comparison = []
        for model_name, pred_info in individual_predictions.items():
            comparison.append({
                'model': model_name,
                'prediction': pred_info['prediction'],
                'confidence': pred_info['confidence'],
                'weight': pred_info['weight'],
                'agrees_with_ensemble': pred_info['prediction'] == ensemble_result['dominant_emotion']
            })
        
        return {
            'ensemble_prediction': ensemble_result,
            'individual_predictions': individual_predictions,
            'model_comparison': comparison,
            'recommended_model': self.get_recommended_model(text)
        } 