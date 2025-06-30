#!/usr/bin/env python3
"""
Test all models and create ensemble predictions
"""

import sys
import os
sys.path.append('backend')

import joblib
import numpy as np
from typing import Dict, List

def test_all_models():
    """Test all models with various examples."""
    
    # Load all models
    models_dir = 'data_and_models/models'
    timestamp = "20250629_231605"
    
    # Load vectorizer
    vectorizer_path = f"{models_dir}/vectorizer_{timestamp}.pkl"
    vectorizer = joblib.load(vectorizer_path)
    print("✅ Vectorizer loaded")
    
    # Load all models
    model_files = {
        'decision_tree': f'decision_tree_{timestamp}.pkl',
        'gradient_boosting': f'gradient_boosting_{timestamp}.pkl',
        'knn': f'knn_{timestamp}.pkl',
        'linear_svc': f'linear_svc_{timestamp}.pkl',
        'logistic_regression': f'logistic_regression_{timestamp}.pkl',
        'naive_bayes': f'naive_bayes_{timestamp}.pkl',
        'random_forest': f'random_forest_{timestamp}.pkl'
    }
    
    models = {}
    for model_name, filename in model_files.items():
        model_path = f"{models_dir}/{filename}"
        models[model_name] = joblib.load(model_path)
        print(f"✅ {model_name} loaded")
    
    # Test cases
    test_cases = [
        ("I am so happy today! Everything went perfectly.", "joy"),
        ("I feel so loved and supported by my friends.", "love"),
        ("I am so angry about what happened at work.", "anger"),
        ("I feel calm and at peace with myself.", "neutral"),
        ("I am scared about the future.", "fear"),
        ("I feel grateful for the opportunities.", "joy"),
        ("I am excited for my vacation!", "joy"),
        ("I feel overwhelmed by all the tasks.", "fear"),
        ("I feel proud of what I accomplished.", "joy"),
        ("I feel nothing in particular today.", "neutral")
    ]
    
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
    
    emotion_labels = ['anger', 'fear', 'joy', 'love', 'neutral', 'sadness', 'surprise']
    
    print("\n" + "="*80)
    print("ENSEMBLE MODEL TESTING")
    print("="*80)
    
    for text, expected in test_cases:
        print(f"\n📝 Text: {text}")
        print(f"🎯 Expected: {expected}")
        
        # Vectorize text
        X = vectorizer.transform([text])
        
        # Get predictions from all models
        predictions = {}
        for model_name, model in models.items():
            try:
                pred = model.predict(X)[0]
                
                # Try to get probabilities
                try:
                    probs = model.predict_proba(X)[0]
                    confidence = max(probs)
                except:
                    confidence = 0.8
                
                predictions[model_name] = {
                    'prediction': pred,
                    'confidence': confidence,
                    'weight': model_weights[model_name]
                }
                
            except Exception as e:
                print(f"❌ Error with {model_name}: {e}")
                predictions[model_name] = {
                    'prediction': 'neutral',
                    'confidence': 0.0,
                    'weight': 0.0
                }
        
        # Calculate ensemble prediction
        emotion_scores = {emotion: 0.0 for emotion in emotion_labels}
        total_weight = 0.0
        
        for model_name, pred_info in predictions.items():
            weight = pred_info['weight']
            total_weight += weight
            
            # Add weighted score for predicted emotion
            emotion_scores[pred_info['prediction']] += weight
        
        # Normalize scores
        if total_weight > 0:
            for emotion in emotion_scores:
                emotion_scores[emotion] /= total_weight
        
        # Get ensemble prediction
        ensemble_prediction = max(emotion_scores.items(), key=lambda x: x[1])[0]
        ensemble_confidence = emotion_scores[ensemble_prediction]
        
        # Calculate model agreement
        pred_list = [pred['prediction'] for pred in predictions.values()]
        agreement = pred_list.count(ensemble_prediction) / len(pred_list)
        
        print(f"🎭 Ensemble Prediction: {ensemble_prediction} (confidence: {ensemble_confidence:.2f})")
        print(f"🤝 Model Agreement: {agreement:.1%}")
        
        # Show individual model predictions
        print("📊 Individual Models:")
        for model_name, pred_info in predictions.items():
            status = "✅" if pred_info['prediction'] == expected else "❌"
            print(f"   {model_name}: {pred_info['prediction']} ({pred_info['confidence']:.2f}) {status}")
        
        # Show if ensemble is correct
        ensemble_status = "✅" if ensemble_prediction == expected else "❌"
        print(f"🎯 Ensemble Result: {ensemble_status}")

if __name__ == "__main__":
    test_all_models() 