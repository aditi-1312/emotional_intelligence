#!/usr/bin/env python3
"""
Script to enhance neutral emotion detection by extracting neutral examples
from the GoEmotions dataset and merging them into our main dataset.
This version adds fewer examples to maintain balance.
"""

import pandas as pd
import numpy as np
from datasets import load_dataset
import logging
from pathlib import Path
import sys

# Add the backend directory to the path
backend_path = Path(__file__).parent.parent / 'backend'
sys.path.append(str(backend_path))

# Import from backend config
sys.path.insert(0, str(backend_path))
from config import DATA_DIR

# Define emotion labels directly
EMOTION_LABELS = ['anger', 'fear', 'joy', 'love', 'neutral', 'sadness', 'surprise']

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_goemotions_dataset():
    """Load the GoEmotions dataset from Hugging Face."""
    try:
        logger.info("Loading GoEmotions dataset...")
        dataset = load_dataset("go_emotions")
        logger.info(f"GoEmotions dataset loaded successfully. Train set size: {len(dataset['train'])}")
        return dataset
    except Exception as e:
        logger.error(f"Error loading GoEmotions dataset: {e}")
        raise

def extract_neutral_examples(dataset, max_examples=500):
    """Extract neutral examples from GoEmotions dataset."""
    logger.info("Extracting neutral examples from GoEmotions...")
    
    neutral_examples = []
    neutral_label_id = 13  # neutral emotion ID in GoEmotions
    
    for example in dataset['train']:
        if len(neutral_examples) >= max_examples:
            break
            
        # Check if this example has neutral emotion
        labels = example['labels']
        if neutral_label_id in labels:
            # Check if it's primarily neutral (not mixed with strong emotions)
            is_neutral = True
            for label_id in labels:
                if label_id != neutral_label_id and label_id in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]:
                    # If it has other emotions, check if neutral is the primary one
                    if len(labels) > 1:
                        is_neutral = False
                        break
            
            if is_neutral:
                text = example['text'].strip()
                if len(text) > 10 and len(text) < 500:  # Reasonable length
                    neutral_examples.append({
                        'text': text,
                        'label': 'neutral',
                        'confidence': 0.9  # High confidence for neutral
                    })
    
    logger.info(f"Extracted {len(neutral_examples)} neutral examples")
    return neutral_examples

def merge_datasets(main_df, neutral_examples):
    """Merge neutral examples into the main dataset."""
    logger.info("Merging neutral examples into main dataset...")
    
    # Convert neutral examples to DataFrame
    neutral_df = pd.DataFrame(neutral_examples)
    
    # Check current neutral distribution
    current_neutral = len(main_df[main_df['label'] == 'neutral'])
    logger.info(f"Current neutral examples in main dataset: {current_neutral}")
    
    # Add neutral examples
    enhanced_df = pd.concat([main_df, neutral_df], ignore_index=True)
    
    # Check new distribution
    new_neutral = len(enhanced_df[enhanced_df['label'] == 'neutral'])
    logger.info(f"New neutral examples in enhanced dataset: {new_neutral}")
    
    # Show overall distribution
    emotion_counts = enhanced_df['label'].value_counts()
    logger.info("Enhanced dataset distribution:")
    for emotion, count in emotion_counts.items():
        percentage = (count / len(enhanced_df)) * 100
        logger.info(f"  {emotion}: {count} ({percentage:.1f}%)")
    
    return enhanced_df

def main():
    """Main function to enhance the dataset."""
    try:
        # Load main dataset
        main_dataset_path = Path(__file__).parent.parent / 'data_and_models' / 'data' / 'emotion_dataset.csv'
        logger.info(f"Loading main dataset from: {main_dataset_path}")
        
        main_df = pd.read_csv(main_dataset_path)
        logger.info(f"Main dataset loaded: {len(main_df)} examples")
        
        # Show current distribution
        logger.info("Current dataset distribution:")
        emotion_counts = main_df['label'].value_counts()
        for emotion, count in emotion_counts.items():
            percentage = (count / len(main_df)) * 100
            logger.info(f"  {emotion}: {count} ({percentage:.1f}%)")
        
        # Load GoEmotions dataset
        goemotions_dataset = load_goemotions_dataset()
        
        # Extract neutral examples (limit to 500 to avoid overfitting)
        neutral_examples = extract_neutral_examples(goemotions_dataset, max_examples=500)
        
        if not neutral_examples:
            logger.warning("No neutral examples found!")
            return
        
        # Merge datasets
        enhanced_df = merge_datasets(main_df, neutral_examples)
        
        # Save enhanced dataset
        enhanced_path = main_dataset_path.parent / 'emotion_dataset_enhanced_balanced.csv'
        enhanced_df.to_csv(enhanced_path, index=False)
        logger.info(f"Enhanced dataset saved to: {enhanced_path}")
        
        # Also save as main dataset
        enhanced_df.to_csv(main_dataset_path, index=False)
        logger.info(f"Enhanced dataset saved as main dataset: {main_dataset_path}")
        
        logger.info("✅ Neutral emotion dataset enhancement completed successfully!")
        
    except Exception as e:
        logger.error(f"Error in main function: {e}")
        raise

if __name__ == "__main__":
    main() 