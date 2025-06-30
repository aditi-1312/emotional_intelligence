#!/usr/bin/env python3
"""
Script to enhance neutral emotion detection by extracting neutral examples
from the GoEmotions dataset and merging them into our main dataset.
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
        logger.info("Loading GoEmotions dataset from Hugging Face...")
        dataset = load_dataset("go_emotions")
        logger.info(f"Loaded GoEmotions dataset with {len(dataset['train'])} training examples")
        return dataset
    except Exception as e:
        logger.error(f"Error loading GoEmotions dataset: {e}")
        return None

def extract_neutral_examples(dataset, target_count=1000):
    """
    Extract neutral examples from GoEmotions dataset.
    
    GoEmotions has 27 emotion labels. We'll consider examples as neutral if:
    1. They have no emotion labels (truly neutral)
    2. They have very low confidence scores for all emotions
    """
    logger.info("Extracting neutral examples from GoEmotions...")
    
    neutral_examples = []
    
    # Get training data
    train_data = dataset['train']
    
    # GoEmotions emotion labels (27 emotions)
    emotion_labels = [
        'admiration', 'amusement', 'anger', 'annoyance', 'approval', 'caring',
        'confusion', 'curiosity', 'desire', 'disappointment', 'disapproval',
        'disgust', 'embarrassment', 'excitement', 'fear', 'gratitude', 'grief',
        'joy', 'love', 'nervousness', 'optimism', 'pride', 'realization',
        'relief', 'remorse', 'sadness', 'surprise', 'neutral'
    ]
    
    # Find examples with no emotion labels or only neutral
    for i, example in enumerate(train_data):
        # Get the emotion labels for this example
        labels = example['labels']
        
        # Check if this is a neutral example
        is_neutral = False
        
        if len(labels) == 0:
            # No emotion labels - truly neutral
            is_neutral = True
        elif len(labels) == 1 and labels[0] == emotion_labels.index('neutral'):
            # Only neutral emotion
            is_neutral = True
        elif len(labels) == 1 and labels[0] == emotion_labels.index('approval'):
            # Approval can be considered somewhat neutral
            is_neutral = True
        
        if is_neutral:
            text = example['text'].strip()
            if len(text) > 10 and len(text) < 500:  # Reasonable length
                neutral_examples.append({
                    'text': text,
                    'label': 'neutral',
                    'confidence': 0.9  # High confidence for neutral
                })
        
        # Stop if we have enough examples
        if len(neutral_examples) >= target_count:
            break
    
    logger.info(f"Extracted {len(neutral_examples)} neutral examples")
    return neutral_examples

def load_main_dataset():
    """Load our main emotion dataset."""
    try:
        dataset_path = DATA_DIR / "emotion_dataset.csv"
        if dataset_path.exists():
            df = pd.read_csv(dataset_path)
            logger.info(f"Loaded main dataset with {len(df)} examples")
            return df
        else:
            logger.error(f"Main dataset not found at {dataset_path}")
            return None
    except Exception as e:
        logger.error(f"Error loading main dataset: {e}")
        return None

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
    logger.info("Enhanced dataset emotion distribution:")
    for emotion, count in emotion_counts.items():
        percentage = (count / len(enhanced_df)) * 100
        logger.info(f"  {emotion}: {count} ({percentage:.1f}%)")
    
    return enhanced_df

def save_enhanced_dataset(df, suffix="_enhanced"):
    """Save the enhanced dataset."""
    try:
        # Create backup of original
        original_path = DATA_DIR / "emotion_dataset.csv"
        backup_path = DATA_DIR / "emotion_dataset_backup.csv"
        
        if original_path.exists():
            import shutil
            shutil.copy2(original_path, backup_path)
            logger.info(f"Created backup at {backup_path}")
        
        # Save enhanced dataset
        enhanced_path = DATA_DIR / f"emotion_dataset{suffix}.csv"
        df.to_csv(enhanced_path, index=False)
        logger.info(f"Saved enhanced dataset at {enhanced_path}")
        
        # Also save as the main dataset
        df.to_csv(original_path, index=False)
        logger.info(f"Updated main dataset at {original_path}")
        
        return enhanced_path
    except Exception as e:
        logger.error(f"Error saving enhanced dataset: {e}")
        return None

def main():
    """Main function to enhance neutral emotion detection."""
    logger.info("Starting neutral emotion dataset enhancement...")
    
    # Load GoEmotions dataset
    goemotions_dataset = load_goemotions_dataset()
    if goemotions_dataset is None:
        logger.error("Failed to load GoEmotions dataset")
        return False
    
    # Extract neutral examples
    neutral_examples = extract_neutral_examples(goemotions_dataset, target_count=2000)
    if not neutral_examples:
        logger.error("No neutral examples extracted")
        return False
    
    # Load main dataset
    main_df = load_main_dataset()
    if main_df is None:
        logger.error("Failed to load main dataset")
        return False
    
    # Merge datasets
    enhanced_df = merge_datasets(main_df, neutral_examples)
    
    # Save enhanced dataset
    enhanced_path = save_enhanced_dataset(enhanced_df)
    if enhanced_path is None:
        logger.error("Failed to save enhanced dataset")
        return False
    
    logger.info("Neutral emotion dataset enhancement completed successfully!")
    logger.info(f"Enhanced dataset saved at: {enhanced_path}")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 