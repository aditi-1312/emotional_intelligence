#!/usr/bin/env python3
"""
Script to download and process the Hugging Face emotion dataset
for retraining the emotion detection models.
"""

import pandas as pd
import numpy as np
from datasets import load_dataset
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_emotion_dataset():
    """Download the Hugging Face emotion dataset."""
    logger.info("Downloading Hugging Face emotion dataset...")
    
    try:
        # Load the dataset
        dataset = load_dataset("dair-ai/emotion")
        logger.info("Dataset downloaded successfully!")
        
        # Convert to pandas DataFrames
        train_df = dataset['train'].to_pandas()
        validation_df = dataset['validation'].to_pandas()
        test_df = dataset['test'].to_pandas()
        
        logger.info(f"Training set: {len(train_df)} samples")
        logger.info(f"Validation set: {len(validation_df)} samples")
        logger.info(f"Test set: {len(test_df)} samples")
        
        return train_df, validation_df, test_df
        
    except Exception as e:
        logger.error(f"Error downloading dataset: {e}")
        return None, None, None

def process_emotion_labels(df):
    """Process emotion labels to match our model's expected format."""
    # Map numeric labels to emotion names
    emotion_mapping = {
        0: 'sadness',
        1: 'joy', 
        2: 'love',
        3: 'anger',
        4: 'fear',
        5: 'surprise'
    }
    
    # Convert numeric labels to emotion names
    df['label'] = df['label'].map(emotion_mapping)
    
    # Add neutral class by sampling from existing emotions
    # We'll add some neutral examples to balance the dataset
    neutral_samples = df.sample(n=min(1000, len(df)//6), random_state=42).copy()
    neutral_samples['label'] = 'neutral'
    neutral_samples['text'] = neutral_samples['text'].apply(lambda x: f"I feel {x.lower()}")
    
    # Combine original data with neutral samples
    df = pd.concat([df, neutral_samples], ignore_index=True)
    
    return df

def balance_dataset(df, samples_per_emotion=2000):
    """Balance the dataset by sampling equal numbers from each emotion."""
    logger.info("Balancing dataset...")
    
    balanced_dfs = []
    emotions = df['label'].unique()
    
    for emotion in emotions:
        emotion_df = df[df['label'] == emotion]
        if len(emotion_df) > samples_per_emotion:
            # Sample if we have too many
            emotion_df = emotion_df.sample(n=samples_per_emotion, random_state=42)
        else:
            # If we have fewer, we'll use all available
            logger.info(f"Emotion '{emotion}': {len(emotion_df)} samples (less than {samples_per_emotion})")
        
        balanced_dfs.append(emotion_df)
    
    balanced_df = pd.concat(balanced_dfs, ignore_index=True)
    
    # Shuffle the dataset
    balanced_df = balanced_df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    logger.info("Dataset balanced successfully!")
    logger.info("Final emotion distribution:")
    for emotion in balanced_df['label'].unique():
        count = len(balanced_df[balanced_df['label'] == emotion])
        logger.info(f"  {emotion}: {count} samples")
    
    return balanced_df

def save_processed_dataset(df, output_path):
    """Save the processed dataset to CSV."""
    logger.info(f"Saving processed dataset to {output_path}")
    
    # Add timestamp column
    df['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Save to CSV
    df.to_csv(output_path, index=False)
    logger.info(f"Dataset saved successfully! Total samples: {len(df)}")
    
    return output_path

def main():
    """Main function to download and process the emotion dataset."""
    logger.info("Starting emotion dataset download and processing...")
    
    # Create output directory if it doesn't exist
    output_dir = "data_and_models/data"
    os.makedirs(output_dir, exist_ok=True)
    
    # Download dataset
    train_df, validation_df, test_df = download_emotion_dataset()
    
    if train_df is None:
        logger.error("Failed to download dataset. Exiting.")
        return
    
    # Process labels
    logger.info("Processing emotion labels...")
    train_df = process_emotion_labels(train_df)
    validation_df = process_emotion_labels(validation_df)
    test_df = process_emotion_labels(test_df)
    
    # Balance the training dataset
    balanced_train_df = balance_dataset(train_df, samples_per_emotion=2000)
    
    # Save processed datasets
    train_path = os.path.join(output_dir, "emotion_dataset_train.csv")
    validation_path = os.path.join(output_dir, "emotion_dataset_validation.csv")
    test_path = os.path.join(output_dir, "emotion_dataset_test.csv")
    
    save_processed_dataset(balanced_train_df, train_path)
    save_processed_dataset(validation_df, validation_path)
    save_processed_dataset(test_df, test_path)
    
    # Create a combined dataset for training
    combined_df = pd.concat([balanced_train_df, validation_df], ignore_index=True)
    combined_path = os.path.join(output_dir, "emotion_dataset.csv")
    save_processed_dataset(combined_df, combined_path)
    
    logger.info("Dataset processing completed successfully!")
    logger.info(f"Files saved:")
    logger.info(f"  - Training: {train_path}")
    logger.info(f"  - Validation: {validation_path}")
    logger.info(f"  - Test: {test_path}")
    logger.info(f"  - Combined: {combined_path}")
    
    # Show sample data
    logger.info("\nSample data:")
    print(combined_df.head(10))
    
    logger.info("\nEmotion distribution in final dataset:")
    emotion_counts = combined_df['label'].value_counts()
    for emotion, count in emotion_counts.items():
        logger.info(f"  {emotion}: {count}")

if __name__ == "__main__":
    main() 