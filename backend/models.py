import pandas as pd
import numpy as np
import joblib
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import logging
from data_processor import EmotionDataProcessor
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    import openai
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    if OPENAI_API_KEY:
        openai.api_key = OPENAI_API_KEY
except ImportError:
    openai = None
    OPENAI_API_KEY = None

class EmotionModelManager:
    """
    Manages ML models for emotion analysis and provides prediction services.
    """
    
    def __init__(self, models_dir: str, data_dir: str):
        """
        Initialize the model manager.
        
        Args:
            models_dir: Path to the directory containing trained models
            data_dir: Path to the directory containing datasets
        """
        self.models_dir = models_dir
        self.data_dir = data_dir
        self.data_processor = EmotionDataProcessor(models_dir, data_dir)
        self.journal_entries = []
        self.emotion_labels = ['anger', 'fear', 'joy', 'love', 'neutral', 'sadness', 'surprise']
        
        # Initialize persistent storage
        self.journal_file = os.path.join(data_dir, 'journal_entries.json')
        self._load_journal_entries()
        
        # Add sample entries if no entries exist
        if not self.journal_entries:
            self._add_sample_entries()
        
    def _load_journal_entries(self):
        """Load journal entries from persistent storage."""
        try:
            if os.path.exists(self.journal_file):
                with open(self.journal_file, 'r') as f:
                    self.journal_entries = json.load(f)
                logger.info(f"Loaded {len(self.journal_entries)} journal entries from storage")
            else:
                self.journal_entries = []
                logger.info("No existing journal entries found, starting fresh")
        except Exception as e:
            logger.error(f"Error loading journal entries: {e}")
            self.journal_entries = []
    
    def _save_journal_entries(self):
        """Save journal entries to persistent storage."""
        try:
            with open(self.journal_file, 'w') as f:
                json.dump(self.journal_entries, f, indent=2, default=str)
            logger.info(f"Saved {len(self.journal_entries)} journal entries to storage")
        except Exception as e:
            logger.error(f"Error saving journal entries: {e}")
    
    def _add_sample_entries(self):
        """Add sample journal entries for demonstration."""
        sample_entries = [
            {
                'id': 1,
                'text': 'Today I feel grateful and happy!',
                'user_id': 'default',
                'timestamp': (datetime.now() - timedelta(days=5)).isoformat(),
                'dominant_emotion': 'joy',
                'confidence': 0.85,
                'emotions': {'joy': 0.85, 'love': 0.10, 'neutral': 0.05},
                'sentiment_score': 0.8,
                'processed_text': 'Today I feel grateful and happy!',
                'ensemble': True,
                'model_agreement': 0.75,
                'models_used': ['linear_svc', 'logistic_regression', 'gradient_boosting']
            },
            {
                'id': 2,
                'text': 'I had a challenging day at work today.',
                'user_id': 'default',
                'timestamp': (datetime.now() - timedelta(days=4)).isoformat(),
                'dominant_emotion': 'sadness',
                'confidence': 0.70,
                'emotions': {'sadness': 0.70, 'fear': 0.20, 'neutral': 0.10},
                'sentiment_score': -0.3,
                'processed_text': 'I had a challenging day at work today.',
                'ensemble': True,
                'model_agreement': 0.60,
                'models_used': ['linear_svc', 'logistic_regression', 'gradient_boosting']
            },
            {
                'id': 3,
                'text': 'I love spending time with my family!',
                'user_id': 'default',
                'timestamp': (datetime.now() - timedelta(days=3)).isoformat(),
                'dominant_emotion': 'love',
                'confidence': 0.90,
                'emotions': {'love': 0.90, 'joy': 0.08, 'neutral': 0.02},
                'sentiment_score': 0.9,
                'processed_text': 'I love spending time with my family!',
                'ensemble': True,
                'model_agreement': 0.85,
                'models_used': ['linear_svc', 'logistic_regression', 'gradient_boosting']
            },
            {
                'id': 4,
                'text': 'I am feeling anxious about the upcoming presentation.',
                'user_id': 'default',
                'timestamp': (datetime.now() - timedelta(days=2)).isoformat(),
                'dominant_emotion': 'fear',
                'confidence': 0.75,
                'emotions': {'fear': 0.75, 'sadness': 0.15, 'neutral': 0.10},
                'sentiment_score': -0.4,
                'processed_text': 'I am feeling anxious about the upcoming presentation.',
                'ensemble': True,
                'model_agreement': 0.70,
                'models_used': ['linear_svc', 'logistic_regression', 'gradient_boosting']
            },
            {
                'id': 5,
                'text': 'I am so excited about my vacation next week!',
                'user_id': 'default',
                'timestamp': (datetime.now() - timedelta(days=1)).isoformat(),
                'dominant_emotion': 'joy',
                'confidence': 0.95,
                'emotions': {'joy': 0.95, 'love': 0.03, 'surprise': 0.02},
                'sentiment_score': 0.9,
                'processed_text': 'I am so excited about my vacation next week!',
                'ensemble': True,
                'model_agreement': 0.90,
                'models_used': ['linear_svc', 'logistic_regression', 'gradient_boosting']
            }
        ]
        
        self.journal_entries = sample_entries
        self._save_journal_entries()
        logger.info("Added 5 sample journal entries for demonstration")
    
    def add_journal_entry(self, text: str, user_id: str = "default") -> Dict:
        """
        Add a new journal entry with emotion analysis.
        
        Args:
            text: Journal entry text
            user_id: User identifier
            
        Returns:
            Dictionary containing the entry with emotion analysis
        """
        if not text or not text.strip():
            raise ValueError("Journal entry text cannot be empty")
        
        # Analyze emotion
        analysis = self.data_processor.analyze_emotion(text)
        sentiment = self.data_processor.get_sentiment_score(text)
        
        # Handle both old and new response formats
        dominant_emotion = analysis.get('dominant_emotion') or analysis.get('emotion', 'neutral')
        confidence = analysis.get('confidence', 0.0)
        emotions = analysis.get('emotions', {})
        
        # Create entry
        entry = {
            'id': len(self.journal_entries) + 1,
            'text': text.strip(),
            'user_id': user_id,
            'timestamp': datetime.now().isoformat(),
            'dominant_emotion': dominant_emotion,
            'confidence': confidence,
            'emotions': emotions,
            'sentiment_score': sentiment,
            'processed_text': analysis.get('processed_text', text.strip()),
            'ensemble': analysis.get('ensemble', False),
            'model_agreement': analysis.get('model_agreement', 0.0),
            'models_used': analysis.get('models_used', [])
        }
        
        # Add to journal
        self.journal_entries.append(entry)
        
        # Keep only recent entries (limit to 1000)
        if len(self.journal_entries) > 1000:
            self.journal_entries = self.journal_entries[-1000:]
        
        # Save to persistent storage
        self._save_journal_entries()
        
        logger.info(f"Added journal entry: {entry['dominant_emotion']} (confidence: {entry['confidence']:.2f})")
        return entry
    
    def get_journal_entries(self, user_id: str = "default", limit: Optional[int] = None) -> List[Dict]:
        """
        Get journal entries for a user.
        
        Args:
            user_id: User identifier
            limit: Maximum number of entries to return
            
        Returns:
            List of journal entries
        """
        entries = [entry for entry in self.journal_entries if entry['user_id'] == user_id]
        
        if limit:
            entries = entries[-limit:]
        
        return entries
    
    def get_analytics_summary(self, user_id: str = "default") -> Dict:
        """
        Get analytics summary for a user's journal entries.
        
        Args:
            user_id: User identifier
            
        Returns:
            Dictionary containing analytics summary
        """
        entries = self.get_journal_entries(user_id)
        
        if not entries:
            return {
                'total_entries': 0,
                'emotion_distribution': {},
                'average_confidence': 0.0,
                'most_common_emotion': 'neutral',
                'recent_emotion': 'neutral',
                'current_mood': 'neutral',
                'sentiment_trend': 'neutral',
                'entries_this_week': 0,
                'entries_this_month': 0
            }
        
        # Get texts for analysis
        texts = [entry['text'] for entry in entries]
        stats = self.data_processor.get_emotion_statistics(texts)
        
        # Get recent emotion
        recent_emotion = entries[-1].get('dominant_emotion', 'neutral') if entries else 'neutral'
        
        # Calculate current mood (average of last 5 entries)
        recent_entries = entries[-5:] if len(entries) >= 5 else entries
        recent_sentiments = [entry.get('sentiment_score', 0.0) for entry in recent_entries]
        avg_sentiment = np.mean(recent_sentiments) if recent_sentiments else 0.0
        
        if avg_sentiment > 0.1:
            current_mood = 'positive'
        elif avg_sentiment < -0.1:
            current_mood = 'negative'
        else:
            current_mood = 'neutral'
        
        # Calculate sentiment trend
        if len(entries) >= 10:
            first_half = entries[:len(entries)//2]
            second_half = entries[len(entries)//2:]
            
            first_sentiment = np.mean([e.get('sentiment_score', 0.0) for e in first_half])
            second_sentiment = np.mean([e.get('sentiment_score', 0.0) for e in second_half])
            
            if second_sentiment > first_sentiment + 0.1:
                sentiment_trend = 'improving'
            elif second_sentiment < first_sentiment - 0.1:
                sentiment_trend = 'declining'
            else:
                sentiment_trend = 'stable'
        else:
            sentiment_trend = 'insufficient_data'
        
        # Count entries by time period
        now = datetime.now()
        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)
        
        entries_this_week = len([e for e in entries 
                               if datetime.fromisoformat(e.get('timestamp', now.isoformat())) >= week_ago])
        entries_this_month = len([e for e in entries 
                                if datetime.fromisoformat(e.get('timestamp', now.isoformat())) >= month_ago])
        
        return {
            'total_entries': stats['total_entries'],
            'emotion_distribution': stats['emotion_distribution'],
            'average_confidence': stats['average_confidence'],
            'most_common_emotion': stats['most_common_emotion'],
            'recent_emotion': recent_emotion,
            'current_mood': current_mood,
            'sentiment_trend': sentiment_trend,
            'entries_this_week': entries_this_week,
            'entries_this_month': entries_this_month,
            'average_sentiment': stats['average_sentiment']
        }
    
    def get_timeline_data(self, user_id: str = "default", limit: int = 30) -> List[Dict]:
        """
        Get timeline data for visualization.
        
        Args:
            user_id: User identifier
            limit: Maximum number of entries to return
            
        Returns:
            List of timeline entries
        """
        entries = self.get_journal_entries(user_id, limit)
        
        timeline_data = []
        for entry in entries:
            timeline_data.append({
                'id': entry.get('id'),
                'text': entry.get('text', ''),
                'timestamp': entry.get('timestamp', ''),
                'emotion': entry.get('dominant_emotion', 'neutral'),
                'confidence': entry.get('confidence', 0.0),
                'sentiment_score': entry.get('sentiment_score', 0.0),
                'date': datetime.fromisoformat(entry.get('timestamp', datetime.now().isoformat())).strftime('%Y-%m-%d') if entry.get('timestamp') else '',
                'time': datetime.fromisoformat(entry.get('timestamp', datetime.now().isoformat())).strftime('%H:%M') if entry.get('timestamp') else ''
            })
        
        return timeline_data
    
    def get_emotion_insights(self, user_id: str = "default") -> Dict:
        """
        Get detailed AI-powered insights about user's emotional patterns.
        If OpenAI API key is set, use GPT to generate comprehensive insights. Otherwise, use fallback logic.
        """
        entries = self.get_journal_entries(user_id)
        if not entries:
            return {
                'intro': "Welcome to your emotional journey! Start by adding some journal entries to get personalized insights.",
                'insights': [],
                'recommendations': [],
                'patterns': {},
                'emotional_journey': {
                    'summary': "Your emotional journey is just beginning. Each entry you make helps us understand your patterns better.",
                    'stats': {
                        'total_entries': 0,
                        'most_common_emotion': 'None yet',
                        'current_mood': 'Neutral',
                        'emotional_clarity': 'Building awareness'
                    }
                }
            }
        
        # If OpenAI is available, use it for detailed insights
        if openai and OPENAI_API_KEY:
            print(f"OpenAI available, API key: {OPENAI_API_KEY[:20]}...")
            try:
                # Prepare detailed journal data for analysis
                journal_texts = []
                emotion_timeline = []
                sentiment_scores = []
                
                for e in entries:
                    journal_texts.append(f"{e.get('timestamp', '')[:10]}: {e.get('text', '')} (Emotion: {e.get('dominant_emotion', 'neutral')}, Confidence: {e.get('confidence', 0.0):.2f})")
                    emotion_timeline.append({
                        'date': e.get('timestamp', '')[:10],
                        'emotion': e.get('dominant_emotion', 'neutral'),
                        'text': e.get('text', ''),
                        'sentiment': e.get('sentiment_score', 0.0)
                    })
                    sentiment_scores.append(e.get('sentiment_score', 0.0))
                
                # Calculate comprehensive patterns for context
                emotion_counts = {}
                recent_entries = entries[-7:] if len(entries) >= 7 else entries
                recent_emotions = [e.get('dominant_emotion', 'neutral') for e in recent_entries]
                
                for entry in entries:
                    emotion = entry.get('dominant_emotion', 'neutral')
                    emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
                
                most_common_emotion = max(emotion_counts.items(), key=lambda x: x[1]) if emotion_counts else None
                avg_sentiment = np.mean(sentiment_scores) if sentiment_scores else 0
                current_mood = recent_entries[-1].get('dominant_emotion', 'neutral') if recent_entries else 'neutral'
                
                # Calculate emotional clarity (variety of emotions expressed)
                unique_emotions = len(set(recent_emotions))
                emotional_clarity = "High awareness" if unique_emotions >= 4 else "Building awareness" if unique_emotions >= 2 else "Developing awareness"
                
                # Enhanced prompt for comprehensive evaluation
                prompt = f"""You are an empathetic mental health counselor with expertise in emotional intelligence and personal growth. 
Analyze the following journal entries and provide a comprehensive, warm evaluation of the user's emotional journey.

JOURNAL ENTRIES:
{chr(10).join(journal_texts)}

EMOTIONAL PATTERNS:
- Most common emotion: {most_common_emotion[0] if most_common_emotion else 'N/A'} ({most_common_emotion[1] if most_common_emotion else 0} times)
- Current mood: {current_mood}
- Average sentiment score: {avg_sentiment:.2f}
- Total entries analyzed: {len(entries)}
- Recent emotional variety: {unique_emotions} different emotions in last 7 entries

Please provide a detailed evaluation in this exact format:

INTRO: [A warm, personalized introduction acknowledging their emotional journey - 2-3 sentences that feel personal and supportive]

INSIGHTS:
1. [Detailed analysis of their most common emotional patterns - what this reveals about their current state and emotional landscape]
2. [Analysis of emotional triggers and situations that affect their mood - specific patterns you notice]
3. [Evaluation of their emotional awareness and self-reflection abilities - how well they understand their emotions]
4. [Assessment of their coping mechanisms and resilience - how they handle different emotional states]
5. [Identification of positive emotional strengths and growth areas - what they're doing well and where they can grow]

RECOMMENDATIONS:
1. [Specific, actionable suggestion for emotional regulation based on their patterns]
2. [Personalized coping strategy that would work well for their specific situation]
3. [Self-care practice recommendation tailored to their emotional needs]
4. [Mindfulness or reflection exercise that addresses their current challenges]
5. [Long-term emotional wellness goal that builds on their strengths]

EMOTIONAL_JOURNEY_SUMMARY: [A 2-3 sentence summary of their overall emotional journey, highlighting progress and potential]

Use a warm, supportive tone. Be specific about their patterns. Include both challenges and strengths. Make recommendations practical and personalized to their situation. Focus on growth and self-compassion."""
                
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an empathetic mental health counselor specializing in emotional intelligence and personal growth. Provide warm, supportive, and detailed analysis that empowers the user."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=1200,
                    temperature=0.7
                )
                
                ai_text = response.choices[0].message.content
                
                # Parse the structured response
                if not ai_text:
                    raise Exception("No response from OpenAI")
                    
                lines = ai_text.strip().split('\n')
                intro = ""
                insights = []
                recommendations = []
                emotional_journey_summary = ""
                
                current_section = None
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    
                    if line.startswith('INTRO:'):
                        current_section = 'intro'
                        intro = line.replace('INTRO:', '').strip()
                    elif line.startswith('INSIGHTS:'):
                        current_section = 'insights'
                    elif line.startswith('RECOMMENDATIONS:'):
                        current_section = 'recommendations'
                    elif line.startswith('EMOTIONAL_JOURNEY_SUMMARY:'):
                        current_section = 'journey_summary'
                        emotional_journey_summary = line.replace('EMOTIONAL_JOURNEY_SUMMARY:', '').strip()
                    elif line.startswith('1.') or line.startswith('2.') or line.startswith('3.') or line.startswith('4.') or line.startswith('5.'):
                        content = line[2:].strip()
                        if current_section == 'insights':
                            insights.append(content)
                        elif current_section == 'recommendations':
                            recommendations.append(content)
                
                return {
                    'intro': intro or "Here's your personalized emotional evaluation:",
                    'insights': insights,
                    'recommendations': recommendations,
                    'patterns': {
                        'emotion_distribution': emotion_counts,
                        'average_sentiment': float(avg_sentiment),
                        'total_entries': len(entries),
                        'most_common_emotion': most_common_emotion[0] if most_common_emotion else None,
                        'current_mood': current_mood,
                        'emotional_clarity': emotional_clarity
                    },
                    'emotional_journey': {
                        'summary': emotional_journey_summary or "Your emotional journey shows growth and self-awareness.",
                        'stats': {
                            'total_entries': len(entries),
                            'most_common_emotion': most_common_emotion[0] if most_common_emotion else 'None',
                            'current_mood': current_mood,
                            'emotional_clarity': emotional_clarity
                        }
                    }
                }
            except Exception as e:
                # Fallback to default logic on error
                print(f"OpenAI error: {e}")
                import traceback
                traceback.print_exc()
                pass
        
        # Fallback logic (enhanced version)
        print("Using fallback logic for insights")
        insights = []
        recommendations = []
        patterns = {}
        
        # Analyze emotion patterns
        emotion_counts = {}
        for entry in entries:
            emotion = entry.get('dominant_emotion', 'neutral')
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        # Most common emotion
        if emotion_counts:
            most_common = max(emotion_counts.items(), key=lambda x: x[1])
            insights.append(f"Your most common emotion is {most_common[0]} ({most_common[1]} times), which suggests this is a significant part of your emotional landscape")
            if most_common[0] in ['sadness', 'anger', 'fear']:
                recommendations.append("Consider practicing mindfulness or talking to someone about your feelings")
            elif most_common[0] in ['joy', 'love']:
                recommendations.append("Your positive emotions are a strength - consider how to cultivate more of these moments")
        
        # Sentiment analysis
        sentiments = [entry.get('sentiment_score', 0.0) for entry in entries]
        avg_sentiment = np.mean(sentiments)
        if avg_sentiment < -0.2:
            insights.append("Your overall sentiment has been negative recently, which is completely normal and part of the human experience")
            recommendations.append("Try focusing on positive activities and gratitude practices")
        elif avg_sentiment > 0.2:
            insights.append("Your overall sentiment has been positive recently - you're doing great work with your emotional well-being")
            recommendations.append("Great job! Keep up the positive mindset and share your good energy with others")
        else:
            insights.append("Your emotional state has been relatively balanced, showing good emotional stability")
            recommendations.append("This balance is healthy - continue to check in with yourself regularly")
        
        # Consistency analysis
        if len(entries) >= 5:
            recent_emotions = [e.get('dominant_emotion', 'neutral') for e in entries[-5:]]
            unique_emotions = len(set(recent_emotions))
            if unique_emotions == 1:
                insights.append("You've been experiencing the same emotion consistently, which might indicate a need for emotional processing")
                if recent_emotions[0] in ['sadness', 'anger']:
                    recommendations.append("Consider trying new activities to shift your emotional state or seeking support")
            elif unique_emotions >= 4:
                insights.append("You've been experiencing a wide range of emotions recently, showing good emotional awareness and flexibility")
                recommendations.append("This emotional variety is normal and healthy - you're processing life's ups and downs well")
        
        # Time patterns
        if len(entries) >= 10:
            morning_entries = []
            evening_entries = []
            for entry in entries:
                hour = datetime.fromisoformat(entry.get('timestamp', datetime.now().isoformat())).hour
                if 6 <= hour < 12:
                    morning_entries.append(entry)
                elif 18 <= hour < 24:
                    evening_entries.append(entry)
            if morning_entries and evening_entries:
                morning_sentiment = np.mean([e.get('sentiment_score', 0.0) for e in morning_entries])
                evening_sentiment = np.mean([e.get('sentiment_score', 0.0) for e in evening_entries])
                if morning_sentiment > evening_sentiment + 0.3:
                    insights.append("You tend to feel better in the mornings, which could be a natural energy pattern for you")
                elif evening_sentiment > morning_sentiment + 0.3:
                    insights.append("You tend to feel better in the evenings, perhaps when you have time to unwind and reflect")
        
        # Current mood and emotional clarity
        current_mood = entries[-1].get('dominant_emotion', 'neutral') if entries else 'neutral'
        recent_emotions = [e.get('dominant_emotion', 'neutral') for e in entries[-7:]] if len(entries) >= 7 else [e.get('dominant_emotion', 'neutral') for e in entries]
        unique_emotions = len(set(recent_emotions))
        emotional_clarity = "High awareness" if unique_emotions >= 4 else "Building awareness" if unique_emotions >= 2 else "Developing awareness"
        
        patterns = {
            'emotion_distribution': emotion_counts,
            'average_sentiment': float(avg_sentiment),
            'total_entries': len(entries),
            'current_mood': current_mood,
            'emotional_clarity': emotional_clarity
        }
        
        return {
            'intro': "Here's your personalized emotional evaluation based on your journal entries:",
            'insights': insights,
            'recommendations': recommendations,
            'patterns': patterns,
            'emotional_journey': {
                'summary': f"Your emotional journey shows {emotional_clarity.lower()} with {len(entries)} entries tracking your growth.",
                'stats': {
                    'total_entries': len(entries),
                    'most_common_emotion': most_common[0] if emotion_counts else 'None',
                    'current_mood': current_mood,
                    'emotional_clarity': emotional_clarity
                }
            }
        }
    
    def predict_emotion(self, text: str, model_name: str = 'ensemble') -> Dict:
        """
        Predict emotion for a given text.
        
        Args:
            text: Text to analyze
            model_name: Name of the model to use ('ensemble' by default)
            
        Returns:
            Dictionary containing prediction results
        """
        analysis = self.data_processor.analyze_emotion(text, model_name)
        
        # Ensure consistent response format
        return {
            'dominant_emotion': analysis.get('dominant_emotion') or analysis.get('emotion', 'neutral'),
            'confidence': analysis.get('confidence', 0.0),
            'emotions': analysis.get('emotions', {}),
            'model_used': analysis.get('model_used', model_name),
            'ensemble': analysis.get('ensemble', False),
            'model_agreement': analysis.get('model_agreement', 0.0),
            'models_used': analysis.get('models_used', []),
            'processed_text': analysis.get('processed_text', text.strip())
        }
    
    def get_model_performance(self) -> Dict:
        """
        Get performance metrics for all models.
        
        Returns:
            Dictionary containing model performance information
        """
        try:
            # Load test data
            dataset = self.data_processor.load_dataset()
            if dataset.empty:
                return {'error': 'Could not load dataset'}
            
            # Split data (simple split for demonstration)
            test_size = min(100, len(dataset) // 5)
            test_data = dataset.tail(test_size)
            
            performance = {}
            
            for model_name in self.data_processor.models.keys():
                correct = 0
                total = 0
                
                for _, row in test_data.iterrows():
                    text = str(row['text'])
                    true_label = row['label']
                    
                    prediction = self.data_processor.analyze_emotion(text, model_name)
                    predicted_label = prediction['dominant_emotion']
                    
                    if predicted_label == true_label:
                        correct += 1
                    total += 1
                
                accuracy = correct / total if total > 0 else 0.0
                performance[model_name] = {
                    'accuracy': accuracy,
                    'correct_predictions': correct,
                    'total_predictions': total
                }
            
            return performance
            
        except Exception as e:
            logger.error(f"Error calculating model performance: {e}")
            return {'error': str(e)} 