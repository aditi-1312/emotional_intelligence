#!/usr/bin/env python3
"""
Enhanced Emotional Intelligence Model Training Script
This script trains multiple models and provides comprehensive analysis
"""

import pandas as pd
import numpy as np
import os
import sys
import time
import warnings
from datetime import datetime
warnings.filterwarnings('ignore')

# Add src to path
sys.path.append('src')

from src.data_processor import AdvancedTextProcessor, FeatureExtractor
from src.models import EmotionClassifier
from src.utils import VisualizationUtils, DataUtils, ModelUtils, ExportUtils
import config

def load_or_generate_data():
    """Load existing dataset or generate sample data"""
    data_path = config.DATA_CONFIG['dataset_path']
    
    if os.path.exists(data_path):
        print(f"Loading existing dataset from {data_path}")
        data = pd.read_csv(data_path)
    else:
        print("No existing dataset found. Generating sample data...")
        data = DataUtils.generate_sample_data(n_samples=config.DATA_CONFIG['sample_size'])
        
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(data_path), exist_ok=True)
        
        # Save dataset
        data.to_csv(data_path, index=False)
        print(f"Sample data saved to {data_path}")
    
    print(f"Dataset shape: {data.shape}")
    print(f"Emotions: {data['label'].unique()}")
    
    return data

def main():
    """Main training function"""
    print("🧠 Enhanced Emotional Intelligence Model Training")
    print("=" * 60)
    print(f"Training started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Step 1: Load or generate data
    print("📊 Step 1: Loading Data...")
    data = load_or_generate_data()
    print()
    
    # Step 2: Initialize classifier
    print("🔧 Step 2: Advanced Text Preprocessing...")
    classifier = EmotionClassifier(models_dir=str(config.MODELS_DIR))
    
    # Step 3: Prepare data
    print("🔍 Step 3: Feature Extraction...")
    X_features, y, processed_data = classifier.prepare_data(
        data, 
        text_column=config.DATA_CONFIG['text_column'],
        label_column=config.DATA_CONFIG['label_column']
    )
    print()
    
    # Step 4: Train models
    print("🤖 Step 4: Training Models...")
    results = classifier.train_models(
        X_features, 
        y,
        test_size=config.DATA_CONFIG['test_size'],
        random_state=config.DATA_CONFIG['random_state']
    )
    print()
    
    # Step 5: Save models
    print("💾 Step 5: Saving Models...")
    classifier.save_models(results, classifier.vectorizer)
    print()
    
    # Step 6: Generate reports
    print("📈 Step 6: Generating Reports...")
    
    # Create results summary
    results_summary = []
    for model_name, result in results.items():
        if result['model'] is not None:
            results_summary.append({
                'Model': model_name,
                'Accuracy': result['accuracy'],
                'Status': 'Success'
            })
        else:
            results_summary.append({
                'Model': model_name,
                'Accuracy': 0.0,
                'Status': 'Failed'
            })
    
    results_df = pd.DataFrame(results_summary)
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_path = os.path.join(config.OUTPUT_DIR, f"training_results_{timestamp}.csv")
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    results_df.to_csv(results_path, index=False)
    
    # Save detailed results
    detailed_results = {
        'best_model': classifier.best_model,
        'best_accuracy': classifier.best_score,
        'training_timestamp': timestamp,
        'dataset_size': len(data),
        'feature_count': X_features.shape[1] if hasattr(X_features, 'shape') else 0,
        'class_count': len(y.unique())
    }
    
    detailed_path = os.path.join(config.OUTPUT_DIR, f"detailed_results_{timestamp}.json")
    ExportUtils.export_results_to_json(detailed_results, detailed_path)
    
    print(f"Results saved to {results_path}")
    print(f"Detailed results saved to {detailed_path}")
    print()
    
    # Step 7: Display summary
    print("📋 TRAINING SUMMARY")
    print("=" * 40)
    print(f"Best Model: {classifier.best_model}")
    print(f"Best Accuracy: {classifier.best_score:.4f}")
    print(f"Total Models Trained: {len([r for r in results.values() if r['model'] is not None])}")
    print(f"Dataset Size: {len(data)} samples")
    print(f"Feature Count: {X_features.shape[1]} features")
    print(f"Classes: {len(y.unique())} emotions")
    print()
    
    # Display model performance
    print("🏆 MODEL PERFORMANCE")
    print("=" * 40)
    for _, row in results_df.iterrows():
        status_icon = "✅" if row['Status'] == 'Success' else "❌"
        print(f"{status_icon} {row['Model']}: {row['Accuracy']:.4f}")
    print()
    
    print("🎉 Training completed successfully!")
    print("\n🚀 Next steps:")
    print("1. Start web interface: streamlit run app.py")
    print("2. Start API server: python api.py")
    print("3. Test the system: python run_demo.py")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Training failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 