#!/usr/bin/env python3
"""
Script to flag and export problematic 'neutral', 'love', and 'surprise' examples for manual review and relabeling.
"""

import pandas as pd
import re
from pathlib import Path

# Define patterns and keywords
FEEL_PATTERNS = [r'^i feel', r'^i am feeling', r'^i dont feel', r'^i didnt feel', r'^i still feel']
LOVE_KEYWORDS = ['love', 'loved', 'loving', 'beloved', 'affection', 'warmth', 'heart']
SURPRISE_KEYWORDS = ['surprised', 'amazed', 'shocked', 'stunned', 'incredible', 'unbelievable', 'wow']
NEUTRAL_KEYWORDS = ['normal', 'okay', 'fine', 'alright', 'ordinary', 'usual', 'regular']

# Load dataset
df = pd.read_csv('../data_and_models/data/emotion_dataset.csv')

# Function to check if text contains any keyword
contains_keyword = lambda text, keywords: any(kw in text.lower() for kw in keywords)

def flag_problematic(row):
    text = row['text'].strip().lower()
    label = row['label']
    # Only flag for target emotions
    if label not in ['neutral', 'love', 'surprise']:
        return False
    # Check if starts with "I feel" or similar
    if not any(re.match(pat, text) for pat in FEEL_PATTERNS):
        return False
    # Check for strong keywords
    if label == 'love' and contains_keyword(text, LOVE_KEYWORDS):
        return False
    if label == 'surprise' and contains_keyword(text, SURPRISE_KEYWORDS):
        return False
    if label == 'neutral' and contains_keyword(text, NEUTRAL_KEYWORDS):
        return False
    return True

# Flag problematic rows
df['problematic'] = df.apply(flag_problematic, axis=1)

# Export problematic rows for manual review
problematic_df = df[df['problematic']]
output_path = Path('../data_and_models/data/problematic_emotion_examples.csv')
problematic_df.to_csv(output_path, index=False)

print(f"Flagged {len(problematic_df)} problematic examples. Exported to {output_path}")
print("You can now review and relabel these in a spreadsheet editor.") 