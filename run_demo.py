#!/usr/bin/env python3
"""
Demo Script for Emotional Intelligence System
Showcases all features and capabilities
"""

import sys
import os
import time
from datetime import datetime

# Add src to path
sys.path.append('src')

def print_banner():
    """Print a beautiful banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║  🧠 Enhanced Emotional Intelligence System Demo 🧠          ║
    ║                                                              ║
    ║  Advanced Text Emotion Analysis & Machine Learning          ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def demo_text_processing():
    """Demo text processing capabilities"""
    print("\n🔧 TEXT PROCESSING DEMO")
    print("=" * 50)
    
    try:
        from src.data_processor import AdvancedTextProcessor
        
        processor = AdvancedTextProcessor()
        
        # Test texts
        test_texts = [
            "I'm feeling REALLY happy today! 😊",
            "I'm so sad and depressed about what happened yesterday.",
            "I'm absolutely FURIOUS about this situation!",
            "I'm scared and anxious about the upcoming exam.",
            "Wow! I'm so SURPRISED by this amazing news!"
        ]
        
        for i, text in enumerate(test_texts, 1):
            print(f"\n{i}. Original: {text}")
            cleaned = processor.clean_text(text)
            print(f"   Cleaned: {cleaned}")
            
            features = processor.extract_text_features(text)
            print(f"   Features: {len(features)} extracted")
            print(f"   - Characters: {features['char_count']}")
            print(f"   - Words: {features['word_count']}")
            print(f"   - Exclamations: {features['exclamation_count']}")
        
        print("\n✅ Text processing demo completed!")
        return True
        
    except Exception as e:
        print(f"❌ Text processing demo failed: {e}")
        return False

def demo_emotion_analysis():
    """Demo emotion analysis capabilities"""
    print("\n🎭 EMOTION ANALYSIS DEMO")
    print("=" * 50)
    
    try:
        from src.models import AdvancedEmotionAnalyzer
        
        analyzer = AdvancedEmotionAnalyzer()
        
        # Test texts with different emotions
        test_cases = [
            ("I'm feeling really happy today! Everything is going great!", "joy"),
            ("I'm so sad and depressed about what happened.", "sadness"),
            ("I'm absolutely furious about this situation!", "anger"),
            ("I'm scared and anxious about the future.", "fear"),
            ("Wow! I'm so surprised by this news!", "surprise"),
            ("I love spending time with my family.", "love"),
            ("The weather is nice today.", "neutral")
        ]
        
        for text, expected_emotion in test_cases:
            print(f"\nText: {text}")
            analysis = analyzer.analyze_text(text)
            dominant_emotion = analyzer.get_dominant_emotion(analysis)
            
            print(f"Expected: {expected_emotion}")
            print(f"Detected: {dominant_emotion}")
            print(f"Emotion counts: {analysis['emotions']}")
            
            # Show features
            features = analysis['features']
            print(f"Text features: {features['word_count']} words, {features['char_count']} chars")
        
        print("\n✅ Emotion analysis demo completed!")
        return True
        
    except Exception as e:
        print(f"❌ Emotion analysis demo failed: {e}")
        return False

def demo_visualization():
    """Demo visualization capabilities"""
    print("\n📊 VISUALIZATION DEMO")
    print("=" * 50)
    
    try:
        from src.utils import VisualizationUtils, DataUtils
        
        # Generate sample data
        print("Generating sample data...")
        data = DataUtils.generate_sample_data(n_samples=200)
        print(f"Generated {len(data)} samples")
        
        # Create visualizations
        print("Creating visualizations...")
        
        # Emotion distribution
        fig1 = VisualizationUtils.create_emotion_distribution_chart(data)
        print("✅ Emotion distribution chart created")
        
        # Text length distribution
        fig2 = VisualizationUtils.create_text_length_distribution(data)
        print("✅ Text length distribution chart created")
        
        # Word cloud
        fig3 = VisualizationUtils.create_word_cloud(data['text'])
        print("✅ Word cloud created")
        
        # Save visualizations
        os.makedirs("output", exist_ok=True)
        fig1.write_html("output/emotion_distribution_demo.html")
        fig2.write_html("output/text_length_demo.html")
        fig3.write_html("output/wordcloud_demo.html")
        
        print("📁 Visualizations saved to output/ directory")
        print("\n✅ Visualization demo completed!")
        return True
        
    except Exception as e:
        print(f"❌ Visualization demo failed: {e}")
        return False

def demo_model_training():
    """Demo model training capabilities"""
    print("\n🤖 MODEL TRAINING DEMO")
    print("=" * 50)
    
    try:
        from src.models import EmotionClassifier
        from src.utils import DataUtils
        
        # Generate training data
        print("Generating training data...")
        data = DataUtils.generate_sample_data(n_samples=1000)
        print(f"Generated {len(data)} training samples")
        
        # Initialize classifier
        classifier = EmotionClassifier()
        models = classifier.get_models()
        print(f"Available models: {list(models.keys())}")
        
        # Show model configurations
        for name, model in models.items():
            print(f"  - {name}: {type(model).__name__}")
        
        print("\n✅ Model training demo completed!")
        print("💡 Run 'python train_models.py' to actually train the models")
        return True
        
    except Exception as e:
        print(f"❌ Model training demo failed: {e}")
        return False

def demo_api_functionality():
    """Demo API functionality"""
    print("\n🌐 API FUNCTIONALITY DEMO")
    print("=" * 50)
    
    try:
        # Test API endpoints
        print("API endpoints available:")
        print("  - POST /analyze - Single text analysis")
        print("  - POST /batch_analyze - Batch text analysis")
        print("  - GET /health - Health check")
        print("  - GET /models - Model information")
        print("  - GET /stats - API statistics")
        
        # Show example curl commands
        print("\nExample API usage:")
        print("  curl -X POST http://localhost:5000/analyze \\")
        print("    -H 'Content-Type: application/json' \\")
        print("    -d '{\"text\": \"I am feeling really happy today!\"}'")
        
        print("\n✅ API functionality demo completed!")
        print("💡 Run 'python api.py' to start the API server")
        return True
        
    except Exception as e:
        print(f"❌ API functionality demo failed: {e}")
        return False

def demo_performance():
    """Demo performance capabilities"""
    print("\n⚡ PERFORMANCE DEMO")
    print("=" * 50)
    
    try:
        from src.models import AdvancedEmotionAnalyzer
        
        analyzer = AdvancedEmotionAnalyzer()
        
        # Test processing speed
        test_text = "I'm feeling really happy today because everything is going well!"
        
        print("Testing processing speed...")
        start_time = time.time()
        
        for i in range(100):
            analysis = analyzer.analyze_text(test_text)
            if i % 20 == 0:
                print(f"  Processed {i+1} texts...")
        
        end_time = time.time()
        total_time = end_time - start_time
        avg_time = total_time / 100
        
        print(f"\nPerformance Results:")
        print(f"  Total time: {total_time:.2f} seconds")
        print(f"  Average time per text: {avg_time:.4f} seconds")
        print(f"  Texts per second: {100/total_time:.1f}")
        
        if avg_time < 0.1:
            print("  Performance: ⭐ Excellent")
        elif avg_time < 0.5:
            print("  Performance: ✅ Good")
        else:
            print("  Performance: ⚠️ Could be improved")
        
        print("\n✅ Performance demo completed!")
        return True
        
    except Exception as e:
        print(f"❌ Performance demo failed: {e}")
        return False

def show_next_steps():
    """Show next steps for using the system"""
    print("\n🚀 NEXT STEPS")
    print("=" * 50)
    
    print("1. 🧠 Train Models:")
    print("   python train_models.py")
    
    print("\n2. 🌐 Start API Server:")
    print("   python api.py")
    print("   Then visit: http://localhost:5000")
    
    print("\n3. 📱 Start Web Interface:")
    print("   streamlit run app.py")
    print("   Then visit: http://localhost:8501")
    
    print("\n4. 🐳 Use Docker (optional):")
    print("   docker-compose up")
    
    print("\n5. 🧪 Run Tests:")
    print("   python test_system.py")
    
    print("\n📚 Documentation:")
    print("   - README.md - Complete documentation")
    print("   - config.py - Configuration options")
    print("   - src/ - Source code documentation")

def main():
    """Main demo function"""
    print_banner()
    
    print(f"Demo started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("This demo showcases all features of the Emotional Intelligence System")
    
    demos = [
        ("Text Processing", demo_text_processing),
        ("Emotion Analysis", demo_emotion_analysis),
        ("Visualization", demo_visualization),
        ("Model Training", demo_model_training),
        ("API Functionality", demo_api_functionality),
        ("Performance", demo_performance)
    ]
    
    results = []
    
    for demo_name, demo_func in demos:
        print(f"\n{'='*20} {demo_name} {'='*20}")
        try:
            result = demo_func()
            results.append((demo_name, result))
        except Exception as e:
            print(f"❌ {demo_name} demo crashed: {e}")
            results.append((demo_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("📋 DEMO SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for demo_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {demo_name}")
    
    print(f"\nOverall: {passed}/{total} demos completed successfully")
    
    if passed == total:
        print("🎉 All demos completed! System is working perfectly.")
    else:
        print("⚠️ Some demos failed. Please check the errors above.")
    
    show_next_steps()
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 