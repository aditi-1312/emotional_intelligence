#!/usr/bin/env python3
"""
Comprehensive test of the ensemble emotion detection system
"""

import requests
import json
from datetime import datetime

def test_ensemble_system():
    """Test the ensemble system with various emotions."""
    
    base_url = "http://localhost:5001"
    
    # Test cases with expected emotions
    test_cases = [
        ("I am so happy today! Everything went perfectly.", "joy"),
        ("I feel so loved and supported by my friends.", "love"),
        ("I am so angry about what happened at work.", "anger"),
        ("I am scared about the future.", "fear"),
        ("I am so sad and lonely today.", "sadness"),
        ("I was surprised by the good news!", "surprise"),
        ("I feel calm and at peace with myself.", "neutral"),
        ("I feel grateful for the opportunities.", "joy"),
        ("I am excited for my vacation!", "joy"),
        ("I feel overwhelmed by all the tasks.", "fear")
    ]
    
    print("🧠 ENSEMBLE EMOTION DETECTION SYSTEM TEST")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    results = []
    correct_predictions = 0
    
    for i, (text, expected) in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}: {text}")
        print(f"🎯 Expected: {expected}")
        
        try:
            # Send request to API
            response = requests.post(
                f"{base_url}/journal",
                json={"text": text},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 201:
                data = response.json()
                entry = data['entry']
                
                predicted = entry['dominant_emotion']
                confidence = entry['confidence']
                model_agreement = entry['model_agreement']
                models_used = entry['models_used']
                ensemble = entry['ensemble']
                
                # Check if prediction is correct
                is_correct = predicted == expected
                if is_correct:
                    correct_predictions += 1
                
                status = "✅" if is_correct else "❌"
                
                print(f"🎭 Predicted: {predicted} {status}")
                print(f"📊 Confidence: {confidence:.2f}")
                print(f"🤝 Model Agreement: {model_agreement:.1%}")
                print(f"🔧 Ensemble: {ensemble}")
                print(f"📈 Models Used: {len(models_used)} models")
                
                results.append({
                    'text': text,
                    'expected': expected,
                    'predicted': predicted,
                    'confidence': confidence,
                    'model_agreement': model_agreement,
                    'correct': is_correct
                })
                
            else:
                print(f"❌ API Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 ENSEMBLE SYSTEM PERFORMANCE SUMMARY")
    print("=" * 60)
    
    total_tests = len(results)
    accuracy = correct_predictions / total_tests if total_tests > 0 else 0
    
    print(f"Total Tests: {total_tests}")
    print(f"Correct Predictions: {correct_predictions}")
    print(f"Accuracy: {accuracy:.1%}")
    
    # Detailed results
    print(f"\n📋 DETAILED RESULTS:")
    print("-" * 60)
    
    for i, result in enumerate(results, 1):
        status = "✅" if result['correct'] else "❌"
        print(f"{i:2d}. {status} Expected: {result['expected']:8s} | Predicted: {result['predicted']:8s} | Confidence: {result['confidence']:.2f} | Agreement: {result['model_agreement']:.1%}")
    
    # Emotion-wise accuracy
    print(f"\n🎭 EMOTION-WISE ACCURACY:")
    print("-" * 60)
    
    emotion_results = {}
    for result in results:
        emotion = result['expected']
        if emotion not in emotion_results:
            emotion_results[emotion] = {'total': 0, 'correct': 0}
        emotion_results[emotion]['total'] += 1
        if result['correct']:
            emotion_results[emotion]['correct'] += 1
    
    for emotion, stats in emotion_results.items():
        accuracy = stats['correct'] / stats['total']
        print(f"{emotion:8s}: {stats['correct']}/{stats['total']} ({accuracy:.1%})")
    
    # Model agreement analysis
    print(f"\n🤝 MODEL AGREEMENT ANALYSIS:")
    print("-" * 60)
    
    agreements = [r['model_agreement'] for r in results]
    avg_agreement = sum(agreements) / len(agreements) if agreements else 0
    
    print(f"Average Model Agreement: {avg_agreement:.1%}")
    print(f"High Agreement (>80%): {sum(1 for a in agreements if a > 0.8)}/{len(agreements)}")
    print(f"Medium Agreement (50-80%): {sum(1 for a in agreements if 0.5 <= a <= 0.8)}/{len(agreements)}")
    print(f"Low Agreement (<50%): {sum(1 for a in agreements if a < 0.5)}/{len(agreements)}")
    
    print(f"\n🎉 ENSEMBLE SYSTEM STATUS: {'EXCELLENT' if accuracy >= 0.8 else 'GOOD' if accuracy >= 0.6 else 'NEEDS IMPROVEMENT'}")
    print("=" * 60)

if __name__ == "__main__":
    test_ensemble_system() 