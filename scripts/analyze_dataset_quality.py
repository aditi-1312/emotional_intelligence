#!/usr/bin/env python3
"""
Script to analyze the quality of our emotion dataset and identify problematic examples.
"""

import pandas as pd
import numpy as np
import re
from collections import Counter

def analyze_emotion_quality(df, emotion):
    """Analyze the quality of examples for a specific emotion."""
    emotion_df = df[df['label'] == emotion]
    
    print(f"\n{'='*50}")
    print(f"ANALYSIS FOR: {emotion.upper()}")
    print(f"{'='*50}")
    print(f"Total examples: {len(emotion_df)}")
    
    # Check for common problematic patterns
    problematic_patterns = {
        'love': ['i feel', 'i am feeling', 'i dont feel', 'i didnt feel'],
        'surprise': ['i feel', 'i am feeling', 'i really feel'],
        'neutral': ['i feel', 'i am feeling', 'i didnt feel', 'i still feel']
    }
    
    if emotion in problematic_patterns:
        print(f"\nProblematic patterns found in {emotion}:")
        for pattern in problematic_patterns[emotion]:
            count = emotion_df['text'].str.contains(pattern, case=False, regex=False).sum()
            if count > 0:
                print(f"  '{pattern}': {count} examples")
    
    # Show sample texts
    print(f"\nSample texts for {emotion}:")
    for i, text in enumerate(emotion_df['text'].head(10), 1):
        print(f"  {i}. {text[:100]}{'...' if len(text) > 100 else ''}")
    
    # Check for emotional keywords that should be present
    emotion_keywords = {
        'love': ['love', 'loved', 'loving', 'beloved', 'affection', 'warmth', 'heart'],
        'surprise': ['surprised', 'amazed', 'shocked', 'stunned', 'incredible', 'unbelievable', 'wow'],
        'neutral': ['normal', 'okay', 'fine', 'alright', 'ordinary', 'usual', 'regular']
    }
    
    if emotion in emotion_keywords:
        print(f"\nExpected keywords for {emotion}:")
        for keyword in emotion_keywords[emotion]:
            count = emotion_df['text'].str.contains(keyword, case=False, regex=False).sum()
            print(f"  '{keyword}': {count} examples")

def main():
    """Main analysis function."""
    # Load dataset
    df = pd.read_csv('../data_and_models/data/emotion_dataset.csv')
    
    print("🧠 EMOTION DATASET QUALITY ANALYSIS")
    print("="*60)
    
    # Overall distribution
    print("\n📊 DATASET DISTRIBUTION:")
    distribution = df['label'].value_counts(normalize=True).round(3) * 100
    for emotion, percentage in distribution.items():
        print(f"  {emotion}: {percentage:.1f}% ({df[df['label'] == emotion].shape[0]} examples)")
    
    # Analyze problematic emotions
    problematic_emotions = ['love', 'surprise', 'neutral']
    
    for emotion in problematic_emotions:
        analyze_emotion_quality(df, emotion)
    
    # Check for generic "I feel" statements
    print(f"\n{'='*50}")
    print("GENERIC 'I FEEL' STATEMENTS ANALYSIS")
    print(f"{'='*50}")
    
    feel_patterns = ['i feel', 'i am feeling', 'i dont feel', 'i didnt feel', 'i still feel']
    
    for pattern in feel_patterns:
        count = df['text'].str.contains(pattern, case=False, regex=False).sum()
        print(f"'{pattern}': {count} total examples")
        
        # Breakdown by emotion
        for emotion in df['label'].unique():
            emotion_count = df[df['label'] == emotion]['text'].str.contains(pattern, case=False, regex=False).sum()
            if emotion_count > 0:
                print(f"  - {emotion}: {emotion_count}")

if __name__ == "__main__":
    main() 