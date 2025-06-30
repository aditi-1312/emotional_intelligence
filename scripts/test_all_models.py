#!/usr/bin/env python3
"""
Script to test all trained emotion detection models and compare their performance.
"""

import sys
import os
sys.path.append(os.path.join('backend'))

from data_processor import EmotionDataProcessor
import pandas as pd

def test_models():
    """Test all models with various emotion examples."""
    
    # Initialize data processor
    models_dir = os.path.join('data_and_models', 'models')
    data_dir = os.path.join('data_and_models', 'data')
    processor = EmotionDataProcessor(models_dir, data_dir)
    
    # Test cases with expected emotions
    test_cases = [
        ("I am so happy today! Everything went perfectly and I feel on top of the world.", "joy"),
        ("I feel so loved and supported by my friends and family.", "love"),
        ("I am so angry about what happened at work today. It was completely unfair.", "anger"),
        ("I am scared about the future and what might happen next.", "fear"),
        ("I am so sad and lonely. Today was a really hard day.", "sadness"),
        ("I was surprised by the good news I received today!", "surprise"),
        ("I feel nothing in particular today. Just an average, uneventful day.", "neutral"),
        ("I feel calm and at peace with myself today.", "neutral"),
        ("I feel grateful for the opportunities I have.", "joy"),
        ("I feel overwhelmed by all the tasks I have to do.", "fear"),
        ("I feel hopeful that things will get better soon.", "joy"),
        ("I feel proud of what I accomplished this week.", "joy"),
        ("I feel anxious about my upcoming exams.", "fear"),
        ("I feel disgusted by the way some people behaved.", "anger"),
        ("I feel excited for my vacation next week!", "joy")
    ]
    
    # Available models
    models = ['logistic_regression', 'random_forest', 'gradient_boosting', 
              'linear_svc', 'naive_bayes', 'knn', 'decision_tree']
    
    results = {}
    
    print("🧠 Testing All Emotion Detection Models")
    print("=" * 60)
    
    for model_name in models:
        print(f"\n📊 Testing {model_name.upper()} model:")
        print("-" * 40)
        
        correct = 0
        total = len(test_cases)
        model_results = []
        
        for text, expected_emotion in test_cases:
            try:
                # Analyze emotion with current model
                result = processor.analyze_emotion(text, model_name)
                predicted_emotion = result['dominant_emotion']
                confidence = result['confidence']
                
                # Check if prediction is correct
                is_correct = predicted_emotion == expected_emotion
                if is_correct:
                    correct += 1
                
                model_results.append({
                    'text': text[:50] + "..." if len(text) > 50 else text,
                    'expected': expected_emotion,
                    'predicted': predicted_emotion,
                    'confidence': confidence,
                    'correct': is_correct
                })
                
                status = "✅" if is_correct else "❌"
                print(f"{status} Expected: {expected_emotion:8} | Predicted: {predicted_emotion:8} | Confidence: {confidence:.3f}")
                
            except Exception as e:
                print(f"❌ Error with {model_name}: {e}")
                model_results.append({
                    'text': text[:50] + "..." if len(text) > 50 else text,
                    'expected': expected_emotion,
                    'predicted': 'ERROR',
                    'confidence': 0.0,
                    'correct': False
                })
        
        accuracy = (correct / total) * 100
        results[model_name] = {
            'accuracy': accuracy,
            'correct': correct,
            'total': total,
            'details': model_results
        }
        
        print(f"\n📈 {model_name.upper()} Accuracy: {accuracy:.1f}% ({correct}/{total})")
    
    # Print summary
    print("\n" + "=" * 60)
    print("🏆 FINAL MODEL COMPARISON")
    print("=" * 60)
    
    # Sort models by accuracy
    sorted_results = sorted(results.items(), key=lambda x: x[1]['accuracy'], reverse=True)
    
    for i, (model_name, result) in enumerate(sorted_results):
        rank = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"{i+1}."
        print(f"{rank} {model_name:20} | Accuracy: {result['accuracy']:5.1f}% | Correct: {result['correct']:2}/{result['total']}")
    
    # Show detailed results for top 3 models
    print("\n" + "=" * 60)
    print("📋 DETAILED RESULTS FOR TOP 3 MODELS")
    print("=" * 60)
    
    for i, (model_name, result) in enumerate(sorted_results[:3]):
        print(f"\n🏆 {model_name.upper()} (Accuracy: {result['accuracy']:.1f}%)")
        print("-" * 50)
        
        for detail in result['details']:
            status = "✅" if detail['correct'] else "❌"
            print(f"{status} {detail['text']}")
            print(f"   Expected: {detail['expected']} | Predicted: {detail['predicted']} | Confidence: {detail['confidence']:.3f}")
    
    return results

def recommend_best_model(results):
    """Recommend the best model based on test results."""
    best_model = max(results.items(), key=lambda x: x[1]['accuracy'])
    
    print("\n" + "=" * 60)
    print("💡 RECOMMENDATION")
    print("=" * 60)
    print(f"🎯 Best Model: {best_model[0].upper()}")
    print(f"📊 Accuracy: {best_model[1]['accuracy']:.1f}%")
    print(f"✅ Correct Predictions: {best_model[1]['correct']}/{best_model[1]['total']}")
    
    # Update the data processor to use the best model
    print(f"\n🔄 To use this model, update the default model in data_processor.py")
    print(f"   Change the default model_name parameter to: '{best_model[0]}'")
    
    return best_model[0]

if __name__ == "__main__":
    results = test_models()
    best_model = recommend_best_model(results) 