import pandas as pd
import numpy as np
import re
import warnings
warnings.filterwarnings('ignore')

# Try to import NLTK components, but handle gracefully if not available
try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer, PorterStemmer
    from nltk.tokenize import word_tokenize
    
    # Download required NLTK data
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        try:
            nltk.download('punkt', quiet=True)
        except:
            pass

    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        try:
            nltk.download('stopwords', quiet=True)
        except:
            pass

    try:
        nltk.data.find('corpora/wordnet')
    except LookupError:
        try:
            nltk.download('wordnet', quiet=True)
        except:
            pass
            
    NLTK_AVAILABLE = True
except:
    NLTK_AVAILABLE = False
    print("Warning: NLTK not available, using simplified text processing")

# Try to import other dependencies
try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except:
    TEXTBLOB_AVAILABLE = False
    print("Warning: TextBlob not available, using simplified sentiment analysis")

try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    VADER_AVAILABLE = True
except:
    VADER_AVAILABLE = False
    print("Warning: VADER not available, using simplified sentiment analysis")

try:
    import textstat
    TEXTSTAT_AVAILABLE = True
except:
    TEXTSTAT_AVAILABLE = False
    print("Warning: textstat not available, using simplified text features")

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

class AdvancedTextProcessor:
    """Enhanced text processor with advanced NLP features"""
    
    def __init__(self, use_lemmatization=True, use_stemming=False):
        self.use_lemmatization = use_lemmatization
        self.use_stemming = use_stemming
        
        # Initialize NLTK components if available
        if NLTK_AVAILABLE:
            try:
                self.lemmatizer = WordNetLemmatizer()
                self.stemmer = PorterStemmer()
                self.stop_words = set(stopwords.words('english'))
            except:
                self.lemmatizer = None
                self.stemmer = None
                self.stop_words = set()
        else:
            self.lemmatizer = None
            self.stemmer = None
            self.stop_words = set()
        
        # Initialize sentiment analyzers if available
        if VADER_AVAILABLE:
            try:
                self.vader_analyzer = SentimentIntensityAnalyzer()
            except:
                self.vader_analyzer = None
        else:
            self.vader_analyzer = None
        
        # Custom stop words for emotional analysis
        self.emotion_stop_words = {
            'really', 'very', 'quite', 'extremely', 'totally', 'completely',
            'absolutely', 'definitely', 'certainly', 'surely', 'obviously'
        }
        self.stop_words.update(self.emotion_stop_words)
    
    def clean_text(self, text):
        """Advanced text cleaning with multiple preprocessing steps"""
        if pd.isna(text) or text == '':
            return ''
        
        # Convert to string and lowercase
        text = str(text).lower()
        
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove special characters but keep apostrophes for contractions
        text = re.sub(r'[^a-zA-Z0-9\s\']', '', text)
        
        # Handle contractions
        text = re.sub(r"n't", " not", text)
        text = re.sub(r"'re", " are", text)
        text = re.sub(r"'s", " is", text)
        text = re.sub(r"'d", " would", text)
        text = re.sub(r"'ll", " will", text)
        text = re.sub(r"'t", " not", text)
        text = re.sub(r"'ve", " have", text)
        text = re.sub(r"'m", " am", text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def tokenize_and_clean(self, text):
        """Tokenize and apply advanced cleaning"""
        if not NLTK_AVAILABLE or self.lemmatizer is None:
            # Simple tokenization without NLTK
            tokens = text.split()
        else:
            try:
                tokens = word_tokenize(text)
            except:
                tokens = text.split()
        
        # Remove stop words and short tokens
        tokens = [token for token in tokens if token not in self.stop_words and len(token) > 2]
        
        # Apply lemmatization or stemming
        if self.use_lemmatization and self.lemmatizer:
            try:
                tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
            except:
                pass
        elif self.use_stemming and self.stemmer:
            try:
                tokens = [self.stemmer.stem(token) for token in tokens]
            except:
                pass
        
        return tokens
    
    def extract_text_features(self, text):
        """Extract comprehensive text features"""
        features = {}
        
        # Basic text statistics
        features['char_count'] = len(text)
        features['word_count'] = len(text.split())
        
        # Sentence count (simplified)
        features['sentence_count'] = len(re.split(r'[.!?]+', text))
        
        # Syllable count (simplified)
        features['syllable_count'] = len(re.findall(r'[aeiouy]+', text.lower()))
        
        # Lexicon count (same as word count for now)
        features['lexicon_count'] = features['word_count']
        
        # Readability scores (simplified)
        if TEXTSTAT_AVAILABLE:
            try:
                features['flesch_reading_ease'] = textstat.flesch_reading_ease(text)
                features['flesch_kincaid_grade'] = textstat.flesch_kincaid_grade(text)
                features['gunning_fog'] = textstat.gunning_fog(text)
                features['smog_index'] = textstat.smog_index(text)
                features['automated_readability_index'] = textstat.automated_readability_index(text)
                features['coleman_liau_index'] = textstat.coleman_liau_index(text)
                features['linsear_write_formula'] = textstat.linsear_write_formula(text)
                features['dale_chall_readability_score'] = textstat.dale_chall_readability_score(text)
            except:
                # Set default values if textstat fails
                features.update({
                    'flesch_reading_ease': 50.0,
                    'flesch_kincaid_grade': 8.0,
                    'gunning_fog': 10.0,
                    'smog_index': 5.0,
                    'automated_readability_index': 8.0,
                    'coleman_liau_index': 8.0,
                    'linsear_write_formula': 8.0,
                    'dale_chall_readability_score': 8.0
                })
        else:
            # Set default values
            features.update({
                'flesch_reading_ease': 50.0,
                'flesch_kincaid_grade': 8.0,
                'gunning_fog': 10.0,
                'smog_index': 5.0,
                'automated_readability_index': 8.0,
                'coleman_liau_index': 8.0,
                'linsear_write_formula': 8.0,
                'dale_chall_readability_score': 8.0
            })
        
        # Sentiment analysis
        if TEXTBLOB_AVAILABLE:
            try:
                blob = TextBlob(text)
                features['polarity'] = blob.sentiment.polarity
                features['subjectivity'] = blob.sentiment.subjectivity
            except:
                features['polarity'] = 0.0
                features['subjectivity'] = 0.5
        else:
            features['polarity'] = 0.0
            features['subjectivity'] = 0.5
        
        # VADER sentiment
        if VADER_AVAILABLE and self.vader_analyzer:
            try:
                vader_scores = self.vader_analyzer.polarity_scores(text)
                features['vader_compound'] = vader_scores['compound']
                features['vader_positive'] = vader_scores['pos']
                features['vader_negative'] = vader_scores['neg']
                features['vader_neutral'] = vader_scores['neu']
            except:
                features.update({
                    'vader_compound': 0.0,
                    'vader_positive': 0.0,
                    'vader_negative': 0.0,
                    'vader_neutral': 1.0
                })
        else:
            features.update({
                'vader_compound': 0.0,
                'vader_positive': 0.0,
                'vader_negative': 0.0,
                'vader_neutral': 1.0
            })
        
        # Emotion indicators
        emotion_words = {
            'joy': ['happy', 'joy', 'excited', 'thrilled', 'delighted', 'pleased'],
            'sadness': ['sad', 'depressed', 'melancholy', 'gloomy', 'miserable', 'sorrowful'],
            'anger': ['angry', 'furious', 'irritated', 'annoyed', 'mad', 'rage'],
            'fear': ['afraid', 'scared', 'terrified', 'anxious', 'worried', 'fearful'],
            'surprise': ['surprised', 'shocked', 'amazed', 'astonished', 'stunned'],
            'disgust': ['disgusted', 'revolted', 'repulsed', 'sickened']
        }
        
        text_lower = text.lower()
        for emotion, words in emotion_words.items():
            features[f'{emotion}_count'] = sum(1 for word in words if word in text_lower)
        
        # Punctuation and formatting features
        features['exclamation_count'] = text.count('!')
        features['question_count'] = text.count('?')
        features['uppercase_count'] = sum(1 for c in text if c.isupper())
        features['digit_count'] = sum(1 for c in text if c.isdigit())
        
        return features
    
    def process_dataset(self, df, text_column='text', label_column='label'):
        """Process entire dataset with advanced features"""
        print("Processing dataset...")
        
        # Clean text
        df['cleaned_text'] = df[text_column].apply(self.clean_text)
        
        # Remove empty texts
        df = df[df['cleaned_text'].str.strip() != ''].reset_index(drop=True)
        
        # Extract text features
        print("Extracting text features...")
        text_features = df['cleaned_text'].apply(self.extract_text_features)
        feature_df = pd.DataFrame(text_features.tolist())
        
        # Combine with original data
        result_df = pd.concat([df, feature_df], axis=1)
        
        print(f"Processed dataset shape: {result_df.shape}")
        return result_df

class FeatureExtractor:
    """Advanced feature extraction for emotional intelligence"""
    
    def __init__(self, max_features=10000, ngram_range=(1, 2)):
        self.max_features = max_features
        self.ngram_range = ngram_range
        self.tfidf_vectorizer = None
        self.count_vectorizer = None
        
    def fit_transform(self, texts):
        """Fit and transform texts using multiple vectorization techniques"""
        # TF-IDF Vectorization
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=self.max_features,
            ngram_range=self.ngram_range,
            stop_words='english',
            min_df=2,
            max_df=0.95
        )
        
        tfidf_features = self.tfidf_vectorizer.fit_transform(texts)
        
        # Count Vectorization for additional features
        self.count_vectorizer = CountVectorizer(
            max_features=self.max_features // 2,
            ngram_range=(1, 1),
            stop_words='english',
            min_df=2,
            max_df=0.95
        )
        
        count_features = self.count_vectorizer.fit_transform(texts)
        
        return tfidf_features, count_features
    
    def transform(self, texts):
        """Transform new texts using fitted vectorizers"""
        if self.tfidf_vectorizer is None or self.count_vectorizer is None:
            raise ValueError("Vectorizers must be fitted first")
        
        tfidf_features = self.tfidf_vectorizer.transform(texts)
        count_features = self.count_vectorizer.transform(texts)
        
        return tfidf_features, count_features 