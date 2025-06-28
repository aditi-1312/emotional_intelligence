import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from wordcloud import WordCloud
import re
import json
from datetime import datetime
import warnings
import io
import base64
from PIL import Image
warnings.filterwarnings('ignore')

class VisualizationUtils:
    """Enhanced utility class for creating various visualizations"""
    
    @staticmethod
    def create_emotion_distribution_chart(data, emotion_column='label'):
        """Create emotion distribution chart"""
        emotion_counts = data[emotion_column].value_counts()
        
        fig = px.pie(
            values=emotion_counts.values,
            names=emotion_counts.index,
            title="Emotion Distribution in Dataset",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        return fig
    
    @staticmethod
    def create_text_length_distribution(data, text_column='text'):
        """Create text length distribution chart"""
        text_lengths = data[text_column].str.len()
        
        fig = px.histogram(
            x=text_lengths,
            title="Text Length Distribution",
            nbins=30,
            color_discrete_sequence=['#1f77b4']
        )
        
        fig.update_layout(
            xaxis_title="Text Length (characters)",
            yaxis_title="Frequency"
        )
        
        return fig
    
    @staticmethod
    def create_word_cloud(text_data, title="Word Cloud"):
        """Create word cloud visualization"""
        # Combine all text
        if isinstance(text_data, pd.Series):
            all_text = " ".join(text_data.tolist())
        else:
            all_text = " ".join(text_data)
        
        # Generate word cloud
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='white',
            colormap='viridis',
            max_words=100
        ).generate(all_text)
        
        # Convert to PIL Image
        wordcloud_image = wordcloud.to_image()
        
        # Convert PIL Image to base64 string
        img_buffer = io.BytesIO()
        wordcloud_image.save(img_buffer, format='PNG')
        img_str = base64.b64encode(img_buffer.getvalue()).decode()
        
        # Create plotly figure with image
        fig = go.Figure()
        
        fig.add_layout_image(
            dict(
                source=f"data:image/png;base64,{img_str}",
                x=0,
                y=1,
                xref="x",
                yref="y",
                sizex=1,
                sizey=1,
                sizing="stretch",
                opacity=1
            )
        )
        
        fig.update_layout(
            title=title,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            width=800,
            height=400
        )
        
        return fig
    
    @staticmethod
    def create_model_comparison_chart(results_df):
        """Create model comparison chart"""
        fig = px.bar(
            results_df,
            x='Model',
            y='Accuracy',
            title="Model Performance Comparison",
            color='Accuracy',
            color_continuous_scale='viridis',
            text='Accuracy'
        )
        
        fig.update_traces(texttemplate='%{text:.3f}', textposition='outside')
        fig.update_layout(
            xaxis_title="Model",
            yaxis_title="Accuracy",
            yaxis_range=[0, 1]
        )
        
        return fig
    
    @staticmethod
    def create_confusion_matrix_heatmap(cm, labels, title="Confusion Matrix"):
        """Create confusion matrix heatmap"""
        fig = px.imshow(
            cm,
            text_auto=True,
            aspect="auto",
            title=title,
            color_continuous_scale='Blues'
        )
        
        fig.update_layout(
            xaxis_title="Predicted",
            yaxis_title="Actual",
            xaxis=dict(tickvals=list(range(len(labels))), ticktext=labels),
            yaxis=dict(tickvals=list(range(len(labels))), ticktext=labels)
        )
        
        return fig
    
    @staticmethod
    def create_emotion_timeline(data, date_column=None, emotion_column='label'):
        """Create emotion timeline chart"""
        if date_column and date_column in data.columns:
            # Group by date and emotion
            timeline_data = data.groupby([date_column, emotion_column]).size().reset_index(name='count')
            
            fig = px.line(
                timeline_data,
                x=date_column,
                y='count',
                color=emotion_column,
                title="Emotion Timeline",
                markers=True
            )
        else:
            # Create sample timeline data
            dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
            emotions = ['joy', 'sadness', 'anger', 'fear', 'surprise', 'love']
            
            timeline_data = []
            for date in dates:
                for emotion in emotions:
                    timeline_data.append({
                        'date': date,
                        'emotion': emotion,
                        'count': np.random.randint(0, 10)
                    })
            
            timeline_df = pd.DataFrame(timeline_data)
            
            fig = px.line(
                timeline_df,
                x='date',
                y='count',
                color='emotion',
                title="Emotion Timeline (Sample Data)",
                markers=True
            )
        
        return fig

class DataUtils:
    """Enhanced utility class for data processing and analysis"""
    
    @staticmethod
    def generate_sample_data(n_samples=1000):
        """Generate sample emotional intelligence data"""
        emotions = ['joy', 'sadness', 'anger', 'fear', 'surprise', 'love', 'neutral']
        
        # Sample texts for each emotion
        emotion_texts = {
            'joy': [
                "I'm feeling so happy today! Everything is going great!",
                "I'm delighted to see you again!",
                "This is absolutely wonderful news!",
                "I'm thrilled about the upcoming vacation!",
                "What a fantastic day this has been!"
            ],
            'sadness': [
                "I'm feeling really sad and depressed today.",
                "I'm so disappointed about what happened.",
                "This makes me feel really down.",
                "I'm feeling quite melancholy today.",
                "I'm really upset about this situation."
            ],
            'anger': [
                "I'm absolutely furious about this!",
                "This makes me so angry and frustrated!",
                "I'm really annoyed by this behavior.",
                "This is completely unacceptable!",
                "I'm so mad about what happened!"
            ],
            'fear': [
                "I'm scared and anxious about the future.",
                "I'm terrified of what might happen.",
                "I'm really worried about this situation.",
                "I'm afraid of the consequences.",
                "I'm feeling quite nervous about this."
            ],
            'surprise': [
                "Wow! I'm so surprised by this news!",
                "I'm absolutely shocked by what happened!",
                "This is completely unexpected!",
                "I'm amazed by this development!",
                "I'm stunned by this revelation!"
            ],
            'love': [
                "I love spending time with my family.",
                "I adore this beautiful place.",
                "I'm so fond of this wonderful person.",
                "I cherish these precious moments.",
                "I'm deeply in love with this."
            ],
            'neutral': [
                "The weather is nice today.",
                "I'm going to the store later.",
                "This is an interesting topic.",
                "I'm thinking about various options.",
                "The meeting was quite informative."
            ]
        }
        
        data = []
        for _ in range(n_samples):
            emotion = np.random.choice(emotions)
            text = np.random.choice(emotion_texts[emotion])
            data.append({
                'text': text,
                'label': emotion,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return pd.DataFrame(data)
    
    @staticmethod
    def analyze_text_complexity(text):
        """Analyze text complexity metrics"""
        # Basic metrics
        char_count = len(text)
        word_count = len(text.split())
        sentence_count = len(re.split(r'[.!?]+', text))
        
        # Average word length
        avg_word_length = char_count / max(word_count, 1)
        
        # Unique words ratio
        unique_words = len(set(text.lower().split()))
        lexical_diversity = unique_words / max(word_count, 1)
        
        # Punctuation analysis
        punctuation_count = len(re.findall(r'[^\w\s]', text))
        punctuation_ratio = punctuation_count / max(char_count, 1)
        
        return {
            'char_count': char_count,
            'word_count': word_count,
            'sentence_count': sentence_count,
            'avg_word_length': avg_word_length,
            'lexical_diversity': lexical_diversity,
            'punctuation_ratio': punctuation_ratio
        }
    
    @staticmethod
    def extract_emotion_keywords(text, emotion_dict):
        """Extract emotion-related keywords from text"""
        text_lower = text.lower()
        found_emotions = {}
        
        for emotion, keywords in emotion_dict.items():
            count = sum(1 for keyword in keywords if keyword in text_lower)
            if count > 0:
                found_emotions[emotion] = count
        
        return found_emotions

class ModelUtils:
    """Enhanced utility class for model-related operations"""
    
    @staticmethod
    def calculate_metrics(y_true, y_pred, y_proba=None):
        """Calculate comprehensive model metrics"""
        from sklearn.metrics import accuracy_score, precision_recall_fscore_support, roc_auc_score
        
        metrics = {}
        
        # Basic accuracy
        metrics['accuracy'] = accuracy_score(y_true, y_pred)
        
        # Precision, recall, f1-score
        precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='weighted')
        metrics['precision'] = precision
        metrics['recall'] = recall
        metrics['f1_score'] = f1
        
        # ROC AUC if probabilities are available
        if y_proba is not None:
            try:
                metrics['roc_auc'] = roc_auc_score(y_true, y_proba, multi_class='ovr')
            except:
                metrics['roc_auc'] = None
        
        return metrics
    
    @staticmethod
    def create_model_report(model_results):
        """Create comprehensive model report"""
        report = {
            'summary': {},
            'detailed_results': {},
            'recommendations': []
        }
        
        # Find best model
        best_model = max(model_results.items(), key=lambda x: x[1]['accuracy'])
        report['summary']['best_model'] = best_model[0]
        report['summary']['best_accuracy'] = best_model[1]['accuracy']
        
        # Average performance
        accuracies = [result['accuracy'] for result in model_results.values()]
        report['summary']['avg_accuracy'] = np.mean(accuracies)
        report['summary']['std_accuracy'] = np.std(accuracies)
        
        # Detailed results
        for model_name, results in model_results.items():
            report['detailed_results'][model_name] = {
                'accuracy': results['accuracy'],
                'training_time': results.get('training_time', 'N/A'),
                'prediction_time': results.get('prediction_time', 'N/A')
            }
        
        # Recommendations
        if report['summary']['best_accuracy'] > 0.8:
            report['recommendations'].append("Excellent model performance achieved!")
        
        if report['summary']['std_accuracy'] < 0.05:
            report['recommendations'].append("Models show consistent performance.")
        
        return report

class ExportUtils:
    """Enhanced utility class for exporting results and reports"""
    
    @staticmethod
    def export_results_to_json(results, filename):
        """Export results to JSON file"""
        # Convert numpy types to native Python types
        def convert_numpy(obj):
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            return obj
        
        # Convert results
        exportable_results = {}
        for key, value in results.items():
            if isinstance(value, dict):
                exportable_results[key] = {k: convert_numpy(v) for k, v in value.items()}
            else:
                exportable_results[key] = convert_numpy(value)
        
        with open(filename, 'w') as f:
            json.dump(exportable_results, f, indent=2, default=str)
    
    @staticmethod
    def export_visualization(fig, filename, format='png'):
        """Export visualization to file"""
        if format == 'png':
            fig.write_image(filename)
        elif format == 'html':
            fig.write_html(filename)
        elif format == 'json':
            fig.write_json(filename)
    
    @staticmethod
    def create_html_report(data, results, visualizations, filename):
        """Create comprehensive HTML report"""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Emotional Intelligence Analysis Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #1f77b4; color: white; padding: 20px; text-align: center; }}
                .section {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; }}
                .metric {{ display: inline-block; margin: 10px; padding: 10px; background-color: #f0f2f6; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Emotional Intelligence Analysis Report</h1>
                <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <div class="section">
                <h2>Dataset Overview</h2>
                <p>Total samples: {len(data)}</p>
                <p>Unique emotions: {data['label'].nunique()}</p>
            </div>
            
            <div class="section">
                <h2>Model Performance</h2>
                <div class="metric">
                    <strong>Best Model:</strong> {results.get('best_model', 'N/A')}
                </div>
                <div class="metric">
                    <strong>Best Accuracy:</strong> {results.get('best_accuracy', 'N/A'):.3f}
                </div>
            </div>
        </body>
        </html>
        """
        
        with open(filename, 'w') as f:
            f.write(html_content)

class AdvancedAnalytics:
    """New class for advanced analytics features"""
    
    @staticmethod
    def calculate_emotion_intensity(text, emotion_keywords):
        """Calculate emotion intensity scores"""
        text_lower = text.lower()
        intensity_scores = {}
        
        for emotion, keywords in emotion_keywords.items():
            # Count keyword occurrences
            keyword_count = sum(1 for keyword in keywords if keyword in text_lower)
            
            # Calculate intensity based on frequency and text length
            text_length = len(text.split())
            intensity = keyword_count / max(text_length, 1)
            
            # Apply exponential scaling for higher intensities
            intensity_scores[emotion] = min(1.0, intensity * 10)
        
        return intensity_scores
    
    @staticmethod
    def detect_emotion_contradictions(text, emotion_scores):
        """Detect conflicting emotions in text"""
        high_emotions = [emotion for emotion, score in emotion_scores.items() if score > 0.3]
        
        # Define emotion contradictions
        contradictions = {
            'joy': ['sadness', 'anger'],
            'sadness': ['joy', 'love'],
            'anger': ['joy', 'love'],
            'fear': ['joy'],
            'surprise': [],  # Surprise can coexist with other emotions
            'love': ['anger', 'fear']
        }
        
        detected_contradictions = []
        for emotion in high_emotions:
            if emotion in contradictions:
                for contradicting_emotion in contradictions[emotion]:
                    if contradicting_emotion in high_emotions:
                        detected_contradictions.append((emotion, contradicting_emotion))
        
        return detected_contradictions
    
    @staticmethod
    def analyze_emotional_progression(texts, timestamps=None):
        """Analyze emotional progression over multiple texts"""
        if timestamps is None:
            timestamps = [datetime.now() for _ in texts]
        
        progression_data = []
        for i, (text, timestamp) in enumerate(zip(texts, timestamps)):
            # Basic emotion analysis (simplified)
            emotion_keywords = {
                'joy': ['happy', 'joy', 'excited', 'great', 'wonderful'],
                'sadness': ['sad', 'depressed', 'unhappy', 'down'],
                'anger': ['angry', 'furious', 'mad', 'rage'],
                'fear': ['afraid', 'scared', 'worried', 'fearful'],
                'surprise': ['surprised', 'shocked', 'amazed'],
                'love': ['love', 'adore', 'cherish']
            }
            
            intensity_scores = AdvancedAnalytics.calculate_emotion_intensity(text, emotion_keywords)
            dominant_emotion = max(intensity_scores.items(), key=lambda x: x[1])[0]
            
            progression_data.append({
                'index': i,
                'timestamp': timestamp,
                'text': text,
                'dominant_emotion': dominant_emotion,
                'intensity_scores': intensity_scores
            })
        
        return progression_data

class PerformanceOptimizer:
    """New class for performance optimization"""
    
    @staticmethod
    def optimize_model_parameters(model_type, X_train, y_train, X_test, y_test):
        """Optimize model hyperparameters using grid search"""
        from sklearn.model_selection import GridSearchCV
        
        param_grids = {
            'logistic_regression': {
                'C': [0.1, 1, 10, 100],
                'solver': ['liblinear', 'lbfgs'],
                'max_iter': [1000]
            },
            'random_forest': {
                'n_estimators': [50, 100, 200],
                'max_depth': [5, 10, 15, None],
                'min_samples_split': [2, 5, 10]
            },
            'svc': {
                'C': [0.1, 1, 10],
                'kernel': ['rbf', 'linear'],
                'gamma': ['scale', 'auto']
            }
        }
        
        if model_type not in param_grids:
            return None
        
        # Import model class
        if model_type == 'logistic_regression':
            from sklearn.linear_model import LogisticRegression
            model = LogisticRegression()
        elif model_type == 'random_forest':
            from sklearn.ensemble import RandomForestClassifier
            model = RandomForestClassifier(random_state=42)
        elif model_type == 'svc':
            from sklearn.svm import SVC
            model = SVC(probability=True, random_state=42)
        
        # Perform grid search
        grid_search = GridSearchCV(
            model, 
            param_grids[model_type], 
            cv=5, 
            scoring='accuracy',
            n_jobs=-1
        )
        
        grid_search.fit(X_train, y_train)
        
        return {
            'best_params': grid_search.best_params_,
            'best_score': grid_search.best_score_,
            'best_model': grid_search.best_estimator_
        }
    
    @staticmethod
    def create_ensemble_model(models, X_train, y_train, voting='soft'):
        """Create ensemble model from multiple trained models"""
        from sklearn.ensemble import VotingClassifier
        
        # Create voting classifier
        ensemble = VotingClassifier(
            estimators=[(f'model_{i}', model) for i, model in enumerate(models)],
            voting=voting
        )
        
        # Train ensemble
        ensemble.fit(X_train, y_train)
        
        return ensemble 