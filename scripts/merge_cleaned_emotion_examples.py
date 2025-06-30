#!/usr/bin/env python3
"""
Script to merge manually cleaned problematic_emotion_examples.csv back into the main emotion_dataset.csv.
Replaces the problematic rows and saves a new cleaned dataset.
"""

import pandas as pd
from pathlib import Path

# Paths
main_path = Path('../data_and_models/data/emotion_dataset.csv')
problematic_path = Path('../data_and_models/data/problematic_emotion_examples.csv')
output_path = Path('../data_and_models/data/emotion_dataset_cleaned.csv')

# Load datasets
main_df = pd.read_csv(main_path)
cleaned_problematic_df = pd.read_csv(problematic_path)

# Remove all problematic rows from main dataset (by index if present, else by text+label match)
if 'problematic' in main_df.columns:
    main_df = main_df[~main_df['problematic']]
else:
    # Remove by text+label match
    problematic_texts = set(cleaned_problematic_df['text'])
    problematic_labels = set(cleaned_problematic_df['label'])
    main_df = main_df[~((main_df['text'].isin(problematic_texts)) & (main_df['label'].isin(problematic_labels)))]

# Concatenate cleaned problematic rows
final_df = pd.concat([main_df, cleaned_problematic_df], ignore_index=True)

# Drop the 'problematic' column if present
if 'problematic' in final_df.columns:
    final_df = final_df.drop(columns=['problematic'])

# Save cleaned dataset
final_df.to_csv(output_path, index=False)
print(f"✅ Merged cleaned problematic examples. Saved new dataset to: {output_path}") 