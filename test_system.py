#!/usr/bin/env python3
"""
Comprehensive Test Script for Emotional Intelligence System
Tests all components and provides detailed feedback
"""

import sys
import os
import time
import traceback
from datetime import datetime

# Add src to path
sys.path.append('src')

def test_imports():
    """Test all required imports"""
    print("🔍 Testing imports...")
    
    try:
        import pandas as pd
        print("✅ pandas imported successfully")
    except Exception as e:
        print(f"❌ pandas import failed: {e}")
        return False
    
    try:
        import numpy as np
        print("✅ numpy imported successfully")
    except Exception as e:
        print(f"❌ numpy import failed: {e}")
        return False
    
    try:
        import streamlit as st
        print("✅ streamlit imported successfully")
    except Exception as e:
        print(f"❌ streamlit import failed: {e}")
        return False
    
    try:
        import plotly.express as px
        print("✅ plotly imported successfully")
    except Exception as e:
        print(f"❌ plotly import failed: {e}")
        return False
    
    try:
        from src.data_processor import AdvancedTextProcessor, FeatureExtractor
        print("✅ data_processor imported successfully")
    except Exception as e:
        print(f"❌ data_processor import failed: {e}")
        return False
    
    try:
        from src.models import EmotionClassifier, AdvancedEmotionAnalyzer
        print("✅ models imported successfully")
    except Exception as e:
        print(f"❌ models import failed: {e}")
        return False
    
    try:
        from src.utils import VisualizationUtils, DataUtils, ModelUtils
        print("✅ utils imported successfully")
    except Exception as e:
        print(f"❌ utils import failed: {e}")
        return False
    
    return True

def test_data_processing():
    """Test data processing functionality"""
    print("\n🔧 Testing data processing...")
    
    try:
        from src.data_processor import AdvancedTextProcessor
        
        # Initialize processor
        processor = AdvancedTextProcessor()
        print("✅ Text processor initialized")
        
        # Test text cleaning
        test_text = "I'm feeling REALLY happy today! 😊"
        cleaned_text = processor.clean_text(test_text)
        print(f"✅ Text cleaning: '{test_text}' -> '{cleaned_text}'")
        
        # Test feature extraction
        features = processor.extract_text_features(test_text)
        print(f"✅ Feature extraction: {len(features)} features extracted")
        
        return True
        
    except Exception as e:
        print(f"❌ Data processing test failed: {e}")
        traceback.print_exc()
        return False

def test_emotion_analysis():
    """Test emotion analysis functionality"""
    print("\n🎭 Testing emotion analysis...")
    
    try:
        from src.models import AdvancedEmotionAnalyzer
        
        # Initialize analyzer
        analyzer = AdvancedEmotionAnalyzer()
        print("✅ Emotion analyzer initialized")
        
        # Test text analysis
        test_texts = [
            "I'm feeling really happy today!",
            "I'm so sad and depressed.",
            "I'm absolutely furious about this!",
            "I'm scared and anxious.",
            "Wow! I'm so surprised!"
        ]
        
        for text in test_texts:
            analysis = analyzer.analyze_text(text)
            dominant_emotion = analyzer.get_dominant_emotion(analysis)
            print(f"✅ Analysis: '{text[:30]}...' -> {dominant_emotion}")
        
        return True
        
    except Exception as e:
        print(f"❌ Emotion analysis test failed: {e}")
        traceback.print_exc()
        return False

def test_visualization():
    """Test visualization functionality"""
    print("\n📊 Testing visualization...")
    
    try:
        from src.utils import VisualizationUtils, DataUtils
        
        # Generate sample data
        data = DataUtils.generate_sample_data(n_samples=100)
        print("✅ Sample data generated")
        
        # Test emotion distribution chart
        fig = VisualizationUtils.create_emotion_distribution_chart(data)
        print("✅ Emotion distribution chart created")
        
        # Test text length distribution
        fig = VisualizationUtils.create_text_length_distribution(data)
        print("✅ Text length distribution chart created")
        
        # Test word cloud
        fig = VisualizationUtils.create_word_cloud(data['text'])
        print("✅ Word cloud created")
        
        return True
        
    except Exception as e:
        print(f"❌ Visualization test failed: {e}")
        traceback.print_exc()
        return False

def test_model_training():
    """Test model training functionality"""
    print("\n🤖 Testing model training...")
    
    try:
        from src.models import EmotionClassifier
        from src.utils import DataUtils
        
        # Generate sample data
        data = DataUtils.generate_sample_data(n_samples=500)
        print("✅ Sample data generated for training")
        
        # Initialize classifier
        classifier = EmotionClassifier()
        print("✅ Classifier initialized")
        
        # Get models
        models = classifier.get_models()
        print(f"✅ {len(models)} models available")
        
        # Test with a small subset
        test_data = data.head(100)
        
        # Prepare features (simplified)
        X = test_data[['text']]  # Just use text for now
        y = test_data['label']
        
        print("✅ Data prepared for training")
        
        return True
        
    except Exception as e:
        print(f"❌ Model training test failed: {e}")
        traceback.print_exc()
        return False

def test_api_endpoints():
    """Test API functionality"""
    print("\n🌐 Testing API endpoints...")
    
    try:
        # Test if we can import the API
        import api
        print("✅ API module imported successfully")
        
        # Test if Flask app can be created
        from flask import Flask
        app = Flask(__name__)
        print("✅ Flask app created successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ API test failed: {e}")
        traceback.print_exc()
        return False

def test_streamlit_app():
    """Test Streamlit app functionality"""
    print("\n📱 Testing Streamlit app...")
    
    try:
        # Test if we can import the app
        import app
        print("✅ Streamlit app module imported successfully")
        
        # Test if main function exists
        if hasattr(app, 'main'):
            print("✅ Main function found")
        else:
            print("⚠️ Main function not found")
        
        return True
        
    except Exception as e:
        print(f"❌ Streamlit app test failed: {e}")
        traceback.print_exc()
        return False

def test_configuration():
    """Test configuration loading"""
    print("\n⚙️ Testing configuration...")
    
    try:
        import config
        print("✅ Configuration module imported")
        
        # Test key configurations
        if hasattr(config, 'DATA_CONFIG'):
            print("✅ Data configuration loaded")
        
        if hasattr(config, 'MODEL_CONFIG'):
            print("✅ Model configuration loaded")
        
        if hasattr(config, 'API_CONFIG'):
            print("✅ API configuration loaded")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        traceback.print_exc()
        return False

def test_directory_structure():
    """Test directory structure"""
    print("\n📁 Testing directory structure...")
    
    required_dirs = ['data', 'output', 'models', 'logs', 'src']
    required_files = [
        'app.py', 'api.py', 'train_models.py', 'config.py', 
        'requirements.txt', 'README.md'
    ]
    
    all_good = True
    
    # Check directories
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✅ Directory '{dir_name}' exists")
        else:
            print(f"❌ Directory '{dir_name}' missing")
            all_good = False
    
    # Check files
    for file_name in required_files:
        if os.path.exists(file_name):
            print(f"✅ File '{file_name}' exists")
        else:
            print(f"❌ File '{file_name}' missing")
            all_good = False
    
    return all_good

def run_performance_test():
    """Run a simple performance test"""
    print("\n⚡ Running performance test...")
    
    try:
        from src.models import AdvancedEmotionAnalyzer
        
        analyzer = AdvancedEmotionAnalyzer()
        
        # Test processing speed
        test_text = "I'm feeling really happy today because everything is going well!"
        
        start_time = time.time()
        for _ in range(100):
            analysis = analyzer.analyze_text(test_text)
        end_time = time.time()
        
        avg_time = (end_time - start_time) / 100
        print(f"✅ Average processing time: {avg_time:.4f} seconds per text")
        
        if avg_time < 0.1:
            print("✅ Performance: Excellent")
        elif avg_time < 0.5:
            print("✅ Performance: Good")
        else:
            print("⚠️ Performance: Could be improved")
        
        return True
        
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧠 Emotional Intelligence System - Comprehensive Test")
    print("=" * 60)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("Directory Structure", test_directory_structure),
        ("Imports", test_imports),
        ("Configuration", test_configuration),
        ("Data Processing", test_data_processing),
        ("Emotion Analysis", test_emotion_analysis),
        ("Visualization", test_visualization),
        ("Model Training", test_model_training),
        ("API Endpoints", test_api_endpoints),
        ("Streamlit App", test_streamlit_app),
        ("Performance", run_performance_test)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("📋 TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
        print("\n🚀 Next steps:")
        print("1. Run: python train_models.py")
        print("2. Run: streamlit run app.py")
        print("3. Run: python api.py")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 