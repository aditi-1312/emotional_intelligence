import pandas as pd
import numpy as np
import pickle
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Import scikit-learn models
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# Import our custom modules
from .data_processor import AdvancedTextProcessor

class EmotionClassifier:
    """Advanced emotion classifier with multiple ML models"""
    
    def __init__(self, models_dir='models'):
        self.models_dir = models_dir
        self.models = {}
        self.vectorizer = None
        self.best_model = None
        self.best_score = 0
        
        # Create models directory if it doesn't exist
        os.makedirs(models_dir, exist_ok=True)
        
        # Initialize models
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize all available models"""
        self.models = {
            'logistic_regression': LogisticRegression(
                random_state=42, max_iter=1000, C=1.0
            ),
            'linear_svc': LinearSVC(
                random_state=42, max_iter=1000, C=1.0
            ),
            'random_forest': RandomForestClassifier(
                n_estimators=100, random_state=42, max_depth=10
            ),
            'gradient_boosting': GradientBoostingClassifier(
                n_estimators=100, random_state=42, max_depth=3
            ),
            'naive_bayes': MultinomialNB(),
            'knn': KNeighborsClassifier(n_neighbors=5),
            'decision_tree': DecisionTreeClassifier(
                random_state=42, max_depth=10
            )
        }
    
    def get_models(self):
        """Get all available models"""
        return self.models
    
    def prepare_data(self, data, text_column='text', label_column='label'):
        """Prepare data for training"""
        print("Preparing data for training...")
        
        # Initialize text processor
        processor = AdvancedTextProcessor()
        
        # Process text data
        processed_data = processor.process_dataset(data, text_column, label_column)
        
        # Prepare features
        X = processed_data['cleaned_text']
        y = processed_data[label_column]
        
        # Initialize TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            stop_words='english',
            min_df=2,
            max_df=0.95
        )
        
        # Transform text to features
        X_features = self.vectorizer.fit_transform(X)
        
        print(f"Feature matrix shape: {X_features.shape}")
        print(f"Number of classes: {len(y.unique())}")
        
        return X_features, y, processed_data
    
    def train_models(self, X, y, test_size=0.2, random_state=42):
        """Train all models and find the best one"""
        print("Training models...")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        results = {}
        
        for name, model in self.models.items():
            print(f"Training {name}...")
            
            try:
                # Train model
                model.fit(X_train, y_train)
                
                # Predict
                y_pred = model.predict(X_test)
                
                # Calculate accuracy
                accuracy = accuracy_score(y_test, y_pred)
                
                results[name] = {
                    'model': model,
                    'accuracy': accuracy,
                    'predictions': y_pred,
                    'true_labels': y_test
                }
                
                print(f"  {name} accuracy: {accuracy:.4f}")
                
                # Update best model
                if accuracy > self.best_score:
                    self.best_score = accuracy
                    self.best_model = name
                
            except Exception as e:
                print(f"  Error training {name}: {e}")
                results[name] = {
                    'model': None,
                    'accuracy': 0.0,
                    'predictions': None,
                    'true_labels': None
                }
        
        print(f"\nBest model: {self.best_model} (accuracy: {self.best_score:.4f})")
        return results
    
    def save_models(self, results, vectorizer=None):
        """Save trained models"""
        print("Saving models...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for name, result in results.items():
            if result['model'] is not None:
                model_path = os.path.join(self.models_dir, f"{name}_{timestamp}.pkl")
                
                # Save model
                with open(model_path, 'wb') as f:
                    pickle.dump(result['model'], f)
                
                print(f"  Saved {name} to {model_path}")
        
        # Save vectorizer
        if vectorizer is not None:
            vectorizer_path = os.path.join(self.models_dir, f"vectorizer_{timestamp}.pkl")
            with open(vectorizer_path, 'wb') as f:
                pickle.dump(vectorizer, f)
            print(f"  Saved vectorizer to {vectorizer_path}")
        
        # Save best model info
        best_model_info = {
            'best_model': self.best_model,
            'best_score': self.best_score,
            'timestamp': timestamp
        }
        
        info_path = os.path.join(self.models_dir, f"best_model_info_{timestamp}.pkl")
        with open(info_path, 'wb') as f:
            pickle.dump(best_model_info, f)
        
        print(f"  Saved best model info to {info_path}")
    
    def load_model(self, model_path):
        """Load a trained model"""
        with open(model_path, 'rb') as f:
            return pickle.load(f)
    
    def predict(self, text, model_name=None):
        """Predict emotion for a single text"""
        if model_name is None:
            model_name = self.best_model
        
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not found")
        
        # Process text
        processor = AdvancedTextProcessor()
        cleaned_text = processor.clean_text(text)
        
        # Vectorize text
        if self.vectorizer is None:
            raise ValueError("Vectorizer not initialized. Please train models first.")
        
        text_features = self.vectorizer.transform([cleaned_text])
        
        # Predict
        model = self.models[model_name]
        prediction = model.predict(text_features)[0]
        probabilities = model.predict_proba(text_features)[0] if hasattr(model, 'predict_proba') else None
        
        return {
            'text': text,
            'cleaned_text': cleaned_text,
            'prediction': prediction,
            'probabilities': probabilities,
            'model_used': model_name
        }

class AdvancedEmotionAnalyzer:
    """Advanced emotion analyzer with rule-based and ML approaches"""
    
    def __init__(self):
        self.emotion_keywords = {
            'joy': [
                'happy', 'joy', 'excited', 'thrilled', 'delighted', 'pleased',
                'ecstatic', 'elated', 'jubilant', 'cheerful', 'glad', 'content',
                'motivated', 'energized', 'energetic', 'pumped', 'fired up',
                'enthusiastic', 'passionate', 'inspired', 'determined', 'confident',
                'optimistic', 'positive', 'amazing', 'wonderful', 'fantastic',
                'brilliant', 'awesome', 'great', 'excellent', 'outstanding',
                'conquer', 'achieve', 'succeed', 'win', 'victory', 'triumph',
                'empowered', 'strong', 'powerful', 'unstoppable', 'invincible',
                # Additional positive motivation keywords
                'boss', 'tackled', 'momentum', 'wave', 'current', 'spirit',
                'accomplished', 'completed', 'finished', 'done', 'checked',
                'progress', 'advancement', 'growth', 'improvement', 'development',
                'breakthrough', 'milestone', 'achievement', 'success', 'accomplishment',
                'fulfilled', 'satisfied', 'proud', 'grateful', 'blessed',
                'lucky', 'fortunate', 'appreciative', 'thankful', 'content',
                'peaceful', 'calm', 'relaxed', 'centered', 'balanced',
                'focused', 'driven', 'ambitious', 'goal-oriented', 'purposeful',
                'meaningful', 'rewarding', 'fulfilling', 'satisfying', 'enjoyable',
                'pleasurable', 'delightful', 'charming', 'lovely', 'beautiful',
                'perfect', 'ideal', 'dream', 'wish', 'hope', 'aspire',
                'strive', 'endeavor', 'pursue', 'chase', 'follow', 'seek'
            ],
            'sadness': [
                'sad', 'depressed', 'melancholy', 'gloomy', 'miserable', 'sorrowful',
                'unhappy', 'down', 'blue', 'dejected', 'despondent', 'heartbroken',
                'hopeless', 'defeated', 'discouraged', 'disappointed', 'let down',
                'lonely', 'isolated', 'abandoned', 'rejected', 'worthless'
            ],
            'anger': [
                'angry', 'furious', 'irritated', 'annoyed', 'mad', 'rage',
                'furious', 'livid', 'enraged', 'outraged', 'fuming', 'livid',
                'frustrated', 'aggravated', 'exasperated', 'infuriated', 'incensed',
                'hostile', 'aggressive', 'violent', 'hate', 'despise', 'loathe'
            ],
            'fear': [
                'afraid', 'scared', 'terrified', 'anxious', 'worried', 'fearful',
                'panicked', 'horrified', 'dread', 'alarmed', 'nervous', 'tense',
                'stressed', 'overwhelmed', 'paranoid', 'suspicious', 'cautious',
                'hesitant', 'uncertain', 'doubtful', 'insecure', 'vulnerable'
            ],
            'surprise': [
                'surprised', 'shocked', 'amazed', 'astonished', 'stunned',
                'bewildered', 'dumbfounded', 'flabbergasted', 'startled',
                'unexpected', 'unbelievable', 'incredible', 'mind-blowing',
                'jaw-dropping', 'staggering', 'overwhelming', 'unforeseen'
            ],
            'love': [
                'love', 'adore', 'cherish', 'fond', 'affectionate', 'tender',
                'passionate', 'romantic', 'devoted', 'caring', 'warm',
                'appreciate', 'grateful', 'thankful', 'blessed', 'lucky',
                'cherished', 'valued', 'respected', 'admired', 'beloved'
            ],
            'disgust': [
                'disgusted', 'revolted', 'repulsed', 'sickened', 'appalled',
                'horrified', 'nauseated', 'repelled', 'offended', 'disgusting',
                'gross', 'nasty', 'vile', 'repulsive', 'abhorrent', 'loathsome'
            ]
        }
        
        # Initialize text processor
        self.processor = AdvancedTextProcessor()
        
        # Emotion intensity modifiers
        self.intensity_modifiers = {
            'very': 1.5,
            'really': 1.5,
            'extremely': 2.0,
            'absolutely': 2.0,
            'completely': 1.8,
            'totally': 1.8,
            'incredibly': 1.7,
            'amazingly': 1.7,
            'slightly': 0.5,
            'somewhat': 0.7,
            'kind of': 0.6,
            'sort of': 0.6
        }
        
        # Positive context indicators (words that suggest positive context)
        self.positive_context_indicators = [
            'like', 'love', 'enjoy', 'appreciate', 'grateful', 'thankful',
            'blessed', 'lucky', 'fortunate', 'amazing', 'wonderful', 'fantastic',
            'great', 'excellent', 'awesome', 'brilliant', 'outstanding',
            'perfect', 'ideal', 'dream', 'wish', 'hope', 'aspire',
            'achieve', 'succeed', 'win', 'victory', 'triumph', 'conquer',
            'momentum', 'wave', 'current', 'spirit', 'energy', 'power',
            'strength', 'confidence', 'determination', 'passion', 'inspiration',
            'motivation', 'drive', 'ambition', 'purpose', 'meaning', 'fulfillment',
            'satisfaction', 'contentment', 'peace', 'calm', 'relaxed',
            'centered', 'balanced', 'focused', 'clear', 'bright', 'light',
            'warm', 'comfortable', 'cozy', 'safe', 'secure', 'protected',
            'supported', 'encouraged', 'inspired', 'motivated', 'energized',
            'pumped', 'fired up', 'ready', 'prepared', 'equipped', 'capable',
            'able', 'skilled', 'talented', 'gifted', 'blessed', 'fortunate'
        ]
        
        # Negative context indicators (words that suggest negative context)
        self.negative_context_indicators = [
            'hate', 'despise', 'loathe', 'abhor', 'detest', 'disgust',
            'repulsed', 'revolted', 'sickened', 'appalled', 'horrified',
            'terrified', 'scared', 'afraid', 'fearful', 'anxious', 'worried',
            'stressed', 'overwhelmed', 'depressed', 'sad', 'miserable',
            'hopeless', 'helpless', 'powerless', 'weak', 'defeated',
            'destroyed', 'ruined', 'broken', 'damaged', 'hurt', 'pain',
            'suffering', 'agony', 'torture', 'nightmare', 'horror', 'terror',
            'panic', 'chaos', 'disaster', 'catastrophe', 'tragedy', 'loss',
            'grief', 'sorrow', 'despair', 'desperation', 'hopelessness',
            'worthlessness', 'uselessness', 'meaninglessness', 'emptiness',
            'loneliness', 'isolation', 'abandonment', 'rejection', 'betrayal',
            'deception', 'lies', 'false', 'fake', 'phony', 'fraud',
            'corruption', 'evil', 'wicked', 'sinful', 'guilty', 'shame',
            'embarrassment', 'humiliation', 'disgrace', 'dishonor', 'disrespect'
        ]
    
    def analyze_text(self, text):
        """Analyze text for emotional content with context-aware detection"""
        if pd.isna(text) or text == '':
            return {
                'text': text,
                'emotions': {},
                'dominant_emotion': 'neutral',
                'confidence': 0.0,
                'features': {}
            }
        
        # Clean text
        cleaned_text = self.processor.clean_text(text)
        
        # Extract text features
        features = self.processor.extract_text_features(text)
        
        # Count emotion keywords
        emotion_counts = {}
        text_lower = cleaned_text.lower()
        
        for emotion, keywords in self.emotion_keywords.items():
            count = 0
            for keyword in keywords:
                count += text_lower.count(keyword)
            emotion_counts[emotion] = count
        
        # Apply context-aware adjustments
        emotion_counts = self._apply_context_adjustments(text_lower, emotion_counts)
        
        # Apply intensity modifiers
        for modifier, multiplier in self.intensity_modifiers.items():
            if modifier in text_lower:
                # Find which emotion this modifier affects
                for emotion in emotion_counts:
                    if any(keyword in text_lower for keyword in self.emotion_keywords[emotion]):
                        emotion_counts[emotion] *= multiplier
        
        # Calculate confidence based on total emotion words
        total_emotion_words = sum(emotion_counts.values())
        confidence = min(1.0, total_emotion_words / 10.0)  # Normalize to 0-1
        
        # Determine dominant emotion
        if total_emotion_words == 0:
            dominant_emotion = 'neutral'
        else:
            dominant_emotion = max(emotion_counts.items(), key=lambda x: x[1])[0]
        
        return {
            'text': text,
            'cleaned_text': cleaned_text,
            'emotions': emotion_counts,
            'dominant_emotion': dominant_emotion,
            'confidence': confidence,
            'features': features,
            'total_emotion_words': total_emotion_words
        }
    
    def _apply_context_adjustments(self, text_lower, emotion_counts):
        """Apply context-aware adjustments to emotion counts"""
        # Count positive and negative context indicators
        positive_context_count = sum(1 for word in self.positive_context_indicators if word in text_lower)
        negative_context_count = sum(1 for word in self.negative_context_indicators if word in text_lower)
        
        # If there's a strong positive context, boost joy and love emotions
        if positive_context_count > negative_context_count:
            emotion_counts['joy'] *= 1.5
            emotion_counts['love'] *= 1.3
            
            # Reduce anger if there are positive context indicators
            if positive_context_count >= 2:
                emotion_counts['anger'] *= 0.3
        
        # If there's a strong negative context, boost negative emotions
        elif negative_context_count > positive_context_count:
            emotion_counts['sadness'] *= 1.3
            emotion_counts['fear'] *= 1.2
            emotion_counts['anger'] *= 1.2
        
        # Special handling for motivational language that might be misclassified as anger
        motivational_indicators = ['boss', 'tackled', 'momentum', 'wave', 'current', 'spirit', 'achieved', 'completed']
        if any(indicator in text_lower for indicator in motivational_indicators):
            # If motivational language is present, boost joy and reduce anger
            emotion_counts['joy'] *= 2.0
            emotion_counts['anger'] *= 0.2
        
        return emotion_counts
    
    def get_dominant_emotion(self, analysis):
        """Get the dominant emotion from analysis"""
        return analysis.get('dominant_emotion', 'neutral')
    
    def get_emotion_scores(self, analysis):
        """Get emotion scores from analysis"""
        return analysis.get('emotions', {})
    
    def analyze_batch(self, texts):
        """Analyze multiple texts"""
        results = []
        for text in texts:
            results.append(self.analyze_text(text))
        return results
    
    def get_emotion_summary(self, analyses):
        """Get summary statistics from multiple analyses"""
        if not analyses:
            return {}
        
        # Count emotions
        emotion_counts = {}
        total_texts = len(analyses)
        
        for analysis in analyses:
            dominant = analysis.get('dominant_emotion', 'neutral')
            emotion_counts[dominant] = emotion_counts.get(dominant, 0) + 1
        
        # Calculate percentages
        emotion_percentages = {
            emotion: (count / total_texts) * 100 
            for emotion, count in emotion_counts.items()
        }
        
        # Average confidence
        avg_confidence = np.mean([
            analysis.get('confidence', 0) for analysis in analyses
        ])
        
        return {
            'total_texts': total_texts,
            'emotion_counts': emotion_counts,
            'emotion_percentages': emotion_percentages,
            'average_confidence': avg_confidence,
            'most_common_emotion': max(emotion_counts.items(), key=lambda x: x[1])[0] if emotion_counts else 'neutral'
        } 