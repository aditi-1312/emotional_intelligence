import pandas as pd
import numpy as np
import re
import os
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Generate timestamp for new model files
TIMESTAMP = datetime.now().strftime('%Y%m%d_%H%M%S')

# Paths
DATA_PATH = os.path.join('..', 'data_and_models', 'data', 'emotion_dataset.csv')
MODELS_DIR = os.path.join('..', 'data_and_models', 'models')

# Model filenames with new timestamp
MODEL_FILES = {
    'vectorizer': f'vectorizer_{TIMESTAMP}.pkl',
    'decision_tree': f'decision_tree_{TIMESTAMP}.pkl',
    'gradient_boosting': f'gradient_boosting_{TIMESTAMP}.pkl',
    'knn': f'knn_{TIMESTAMP}.pkl',
    'linear_svc': f'linear_svc_{TIMESTAMP}.pkl',
    'logistic_regression': f'logistic_regression_{TIMESTAMP}.pkl',
    'naive_bayes': f'naive_bayes_{TIMESTAMP}.pkl',
    'random_forest': f'random_forest_{TIMESTAMP}.pkl'
}

# Clean text function
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def main():
    print('Loading new Hugging Face emotion dataset...')
    df = pd.read_csv(DATA_PATH)
    if 'text' not in df.columns or 'label' not in df.columns:
        raise ValueError('Dataset must have "text" and "label" columns')
    
    print(f"Original dataset shape: {df.shape}")
    print(f"Emotion distribution:")
    print(df['label'].value_counts())
    
    # Clean text
    df['text'] = df['text'].astype(str).apply(clean_text)
    df = df[df['text'].str.strip() != '']
    print(f"Data shape after cleaning: {df.shape}")

    X = df['text']
    y = df['label']

    print('Vectorizing text...')
    vectorizer = TfidfVectorizer(
        stop_words='english', 
        max_features=15000, 
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.95
    )
    X_vect = vectorizer.fit_transform(X)
    joblib.dump(vectorizer, os.path.join(MODELS_DIR, MODEL_FILES['vectorizer']))
    print('Vectorizer saved.')

    X_train, X_test, y_train, y_test = train_test_split(
        X_vect, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"Training set size: {X_train.shape[0]}")
    print(f"Test set size: {X_test.shape[0]}")

    models = {
        'logistic_regression': LogisticRegression(max_iter=2000, solver='liblinear', C=1.0),
        'random_forest': RandomForestClassifier(n_estimators=200, random_state=42, max_depth=20),
        'gradient_boosting': GradientBoostingClassifier(n_estimators=200, random_state=42, max_depth=6),
        'linear_svc': LinearSVC(max_iter=2000, random_state=42, C=1.0),
        'naive_bayes': MultinomialNB(alpha=0.1),
        'knn': KNeighborsClassifier(n_neighbors=7, weights='distance'),
        'decision_tree': DecisionTreeClassifier(random_state=42, max_depth=15)
    }

    best_model = None
    best_accuracy = 0
    results = {}

    for name, model in models.items():
        print(f'\nTraining {name}...')
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        results[name] = acc
        
        print(f"{name} accuracy: {acc:.4f}")
        print(classification_report(y_test, preds))
        
        # Save model
        joblib.dump(model, os.path.join(MODELS_DIR, MODEL_FILES[name]))
        print(f"{name} saved.")
        
        if acc > best_accuracy:
            best_accuracy = acc
            best_model = name

    print(f'\n=== TRAINING COMPLETED ===')
    print(f'Best model: {best_model} (accuracy: {best_accuracy:.4f})')
    print(f'All models saved with timestamp: {TIMESTAMP}')
    
    # Save model info
    model_info = {
        'timestamp': TIMESTAMP,
        'best_model': best_model,
        'best_accuracy': best_accuracy,
        'results': results,
        'dataset_size': len(df),
        'emotion_distribution': df['label'].value_counts().to_dict()
    }
    
    model_info_path = os.path.join(MODELS_DIR, f'best_model_info_{TIMESTAMP}.pkl')
    joblib.dump(model_info, model_info_path)
    print(f'Model info saved to: {model_info_path}')
    
    # Print summary
    print(f'\nModel Performance Summary:')
    for name, acc in sorted(results.items(), key=lambda x: x[1], reverse=True):
        print(f'  {name}: {acc:.4f}')

if __name__ == '__main__':
    main() 