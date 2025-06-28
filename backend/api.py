#!/usr/bin/env python3
"""
Flask API for Emotional Intelligence Analysis
Provides RESTful endpoints for emotion analysis
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import os
import sys
import joblib
from datetime import datetime
import logging
from collections import Counter
import requests
import json

# Add src to path
sys.path.append('src')

from src.data_processor import AdvancedTextProcessor
from src.models import AdvancedEmotionAnalyzer
from src.utils import DataUtils

# Load environment variables
from dotenv import load_dotenv
load_dotenv('config.env')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

# Enable CORS
CORS(app)

# Initialize components
try:
    processor = AdvancedTextProcessor()
    analyzer = AdvancedEmotionAnalyzer()
    data_utils = DataUtils()
    logger.info("Initialized emotion analyzer")
except Exception as e:
    logger.error(f"Error initializing components: {e}")

# In-memory storage for demo (replace with database in production)
journal_entries = []
entry_id_counter = 1

def get_ai_insights(analytics_data):
    """
    Generate AI insights using ChatGPT API or fallback to rule-based insights
    """
    try:
        # Try to use ChatGPT API if available
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if openai_api_key:
            return get_chatgpt_insights(analytics_data, openai_api_key)
        else:
            return get_rule_based_insights(analytics_data)
    except Exception as e:
        logger.error(f"Error generating AI insights: {e}")
        return get_rule_based_insights(analytics_data)

def get_chatgpt_insights(analytics_data, api_key):
    """
    Generate personalized insights using ChatGPT API
    """
    try:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Get recent journal entries for context
        recent_entries = []
        user_id = 'user123'  # Default user
        user_entries = [entry for entry in journal_entries if entry['user_id'] == user_id]
        user_entries.sort(key=lambda x: x['timestamp'], reverse=True)
        
        # Get last 3 entries for context
        for entry in user_entries[:3]:
            recent_entries.append({
                'text': entry['text'][:200] + '...' if len(entry['text']) > 200 else entry['text'],
                'emotion': entry['emotion'],
                'date': entry['timestamp'][:10]
            })
        
        # Create a more detailed and personalized prompt
        prompt = f"""
        You are a compassionate, empathetic mental health companion. Based on this person's mood tracking data, provide personalized, warm, and supportive insights.

        **Their Journey So Far:**
        - They've been journaling for {analytics_data['total_entries']} days
        - Their most frequent emotion: {analytics_data['most_common_emotion']}
        - Their current mood: {analytics_data['recent_emotion']}
        - Their emotional clarity: {analytics_data['average_confidence']:.1%}
        - Their emotional landscape: {analytics_data['emotion_distribution']}

        **Recent Reflections:**
        {chr(10).join([f"• {entry['date']}: {entry['emotion']} - \"{entry['text']}\"" for entry in recent_entries])}

        **Please provide:**
        1. **A warm, personal reflection** on their emotional journey
        2. **Specific insights** about their patterns and what they might mean
        3. **Gentle, actionable suggestions** tailored to their current state
        4. **Words of encouragement** that feel like they're coming from a caring friend
        5. **When to consider professional support** (if relevant)

        **Tone Guidelines:**
        - Be warm, personal, and conversational
        - Use "you" and speak directly to them
        - Acknowledge their feelings as valid
        - Offer hope and encouragement
        - Be specific about their situation, not generic advice
        - Use emojis sparingly but warmly
        - Keep it under 300 words

        Remember: You're speaking to someone who's been brave enough to track their emotions. Honor that courage with genuine care and understanding.
        """
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a warm, empathetic mental health companion who provides personalized, supportive insights. You speak like a caring friend who truly understands emotional journeys. You're encouraging, specific, and genuinely helpful."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 600,
            "temperature": 0.8
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=15)
        response.raise_for_status()
        
        result = response.json()
        insights = result['choices'][0]['message']['content']
        return insights
        
    except Exception as e:
        logger.error(f"ChatGPT API error: {e}")
        return get_rule_based_insights(analytics_data)

def get_rule_based_insights(analytics_data):
    """
    Generate personalized insights using rule-based approach
    """
    total_entries = analytics_data['total_entries']
    most_common = analytics_data['most_common_emotion']
    recent_emotion = analytics_data['recent_emotion']
    avg_confidence = analytics_data['average_confidence']
    emotion_dist = analytics_data['emotion_distribution']
    
    # Get recent entries for context
    recent_entries = []
    user_id = 'user123'
    user_entries = [entry for entry in journal_entries if entry['user_id'] == user_id]
    user_entries.sort(key=lambda x: x['timestamp'], reverse=True)
    
    if user_entries:
        recent_text = user_entries[0]['text'][:100] + '...' if len(user_entries[0]['text']) > 100 else user_entries[0]['text']
    else:
        recent_text = "your recent reflections"
    
    insights = f"I've been following your emotional journey through {total_entries} journal entries, and I want to share some personal reflections with you.\n\n"
    
    # Personalized emotion analysis
    if most_common == 'joy':
        insights += f"🌟 I've noticed joy has been a constant companion in your life lately. That's beautiful! Your recent entry about \"{recent_text}\" shows this positive energy. When joy flows naturally like this, it often means you're aligned with what truly matters to you. Consider what's been fueling this happiness - maybe it's certain activities, people, or moments of achievement?\n\n"
    elif most_common == 'sadness':
        insights += f"💙 I see sadness has been present in your journey. Your recent reflection about \"{recent_text}\" touches on this. Remember, feeling sad doesn't mean you're doing anything wrong - it's a natural part of being human. Sometimes sadness is our heart's way of processing change or loss. What would feel most supportive to you right now?\n\n"
    elif most_common == 'anger':
        insights += f"🔥 Anger has been showing up in your entries, including your recent thoughts about \"{recent_text}\". Anger often signals that something important to you feels threatened or unfair. It can be a powerful catalyst for change when channeled mindfully. What might your anger be trying to tell you about your needs or boundaries?\n\n"
    elif most_common == 'fear':
        insights += f"😰 I've noticed fear and anxiety appearing in your reflections, like in your recent entry about \"{recent_text}\". These feelings are incredibly common and often arise when we're facing uncertainty or change. Your brain is trying to protect you, even if it feels overwhelming. What small steps could help you feel more grounded?\n\n"
    elif most_common == 'surprise':
        insights += f"😲 Your emotional landscape has been full of surprises! Your recent reflection about \"{recent_text}\" captures this sense of the unexpected. Life has been throwing you curveballs, and you're navigating them with curiosity. This adaptability is a real strength - you're learning to dance with uncertainty.\n\n"
    elif most_common == 'disgust':
        insights += f"🤢 I see disgust has been present in your journey, including your recent thoughts about \"{recent_text}\". This emotion often arises when something feels fundamentally wrong or out of alignment with your values. It might be signaling that certain aspects of your life need attention or change.\n\n"
    elif most_common == 'love':
        insights += f"❤️ Love has been flowing through your entries! Your recent reflection about \"{recent_text}\" radiates this warmth. When love is your dominant emotion, it often means you're deeply connected to what matters most. This connection is precious - how can you nurture it further?\n\n"
    elif most_common == 'neutral':
        insights += f"😐 I've noticed you've been in a more neutral space lately, including your recent entry about \"{recent_text}\". Sometimes this calm center is exactly what we need - a place to rest and reset. It can also be a sign that you're processing deeper emotions beneath the surface.\n\n"
    
    # Analyze emotional shifts
    if recent_emotion != most_common:
        if recent_emotion == 'joy' and most_common != 'joy':
            insights += f"✨ I love seeing this shift toward joy in your recent entry! This change suggests something positive is happening in your life. What's been different lately that might be contributing to this brighter energy?\n\n"
        elif recent_emotion == 'sadness' and most_common != 'sadness':
            insights += f"💙 I notice you're feeling sadder than usual lately. This shift is completely normal - emotions ebb and flow like waves. Your feelings are valid, and it's okay to need extra care during these times. What would feel most comforting to you right now?\n\n"
        else:
            insights += f"📊 I see your emotional energy has shifted from {most_common} to {recent_emotion}. This change might reflect new circumstances, insights, or simply the natural flow of your inner world. How are you feeling about this shift?\n\n"
    
    # Emotional clarity insights
    if avg_confidence > 0.8:
        insights += "🎯 Your journal entries have such clarity and depth - the emotion detection really connects with what you're sharing. This suggests you have a strong emotional vocabulary and self-awareness. That's a real gift!\n\n"
    elif avg_confidence > 0.6:
        insights += "📝 Your emotional landscape has some beautiful complexity to it. Sometimes emotions blend together, and that's perfectly normal. You might be experiencing mixed feelings, which shows the richness of your inner world.\n\n"
    else:
        insights += "🤔 I notice the emotion detection sometimes struggles to capture the full picture of your feelings. This might mean your emotions are beautifully complex or that you're experiencing subtle nuances that are hard to categorize. That's actually quite normal - emotions rarely fit into neat boxes!\n\n"
    
    # Personalized encouragement based on patterns
    joy_count = emotion_dist.get('joy', 0)
    if joy_count > total_entries * 0.4:
        insights += "🌟 You seem to have a natural capacity for joy and positivity. This is a wonderful foundation for resilience and well-being. Keep nurturing whatever brings you this light!\n\n"
    
    if emotion_dist.get('sadness', 0) > total_entries * 0.3:
        insights += "💙 I see you've been through some challenging emotional terrain. Your courage in facing these feelings head-on is truly admirable. Remember, you don't have to navigate this alone.\n\n"
    
    # Gentle, actionable suggestions
    insights += "💡 Here are some gentle suggestions that might resonate with where you are:\n"
    
    if recent_emotion in ['sadness', 'fear']:
        insights += "• Try a simple grounding exercise: name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, 1 you can taste\n"
        insights += "• Reach out to someone you trust - even a brief connection can help\n"
        insights += "• Give yourself permission to rest and be gentle with yourself\n"
    elif recent_emotion == 'joy':
        insights += "• Savor these positive moments - maybe take a mental snapshot\n"
        insights += "• Consider what's working well and how you can create more of it\n"
        insights += "• Share your good energy with someone who might need it\n"
    elif recent_emotion == 'anger':
        insights += "• Try some physical movement to release the energy\n"
        insights += "• Write down what's bothering you, then what you need\n"
        insights += "• Practice deep breathing - 4 counts in, 6 counts out\n"
    else:
        insights += "• Take a few moments to check in with yourself each day\n"
        insights += "• Notice what activities help you feel most like yourself\n"
        insights += "• Be curious about your emotions without judging them\n"
    
    insights += "\n💝 Remember: You're doing the brave work of understanding yourself. Every entry you write is a step toward greater self-awareness and emotional well-being. That's something to be proud of.\n\n"
    
    # Professional support guidance
    if emotion_dist.get('sadness', 0) > total_entries * 0.5 or emotion_dist.get('fear', 0) > total_entries * 0.4:
        insights += "🤗 If these feelings start to feel overwhelming or interfere with your daily life, consider reaching out to a mental health professional. Seeking support is a sign of strength and self-care.\n\n"
    
    return insights

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'message': 'Emotional Intelligence API is running'
    })

@app.route('/', methods=['GET'])
def index():
    """Root endpoint"""
    return jsonify({
        'message': 'Emotional Intelligence API',
        'endpoints': {
            'health': '/health',
            'analyze': '/analyze',
            'journal': '/journal',
            'analytics': '/analytics/summary',
            'timeline': '/analytics/timeline',
            'ai_insights': '/ai/insights'
        }
    })

@app.route('/analyze', methods=['POST'])
def analyze_text():
    """Analyze text for emotion"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        # Analyze the text
        analysis = analyzer.analyze_text(text)
        
        return jsonify({
            'text': text,
            'analysis': analysis
        })
        
    except Exception as e:
        logger.error(f"Error analyzing text: {e}")
        return jsonify({'error': 'Analysis failed'}), 500

@app.route('/journal', methods=['POST'])
def add_journal_entry():
    """Add a new journal entry"""
    global entry_id_counter
    
    try:
        data = request.get_json()
        text = data.get('text', '')
        user_id = data.get('user_id', 'user123')
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        # Analyze the text
        analysis = analyzer.analyze_text(text)
        
        # Create journal entry
        entry = {
            'id': entry_id_counter,
            'user_id': user_id,
            'text': text,
            'emotion': analysis['dominant_emotion'],
            'confidence': analysis['confidence'],
            'timestamp': datetime.now().isoformat(),
            'analysis': analysis
        }
        
        journal_entries.append(entry)
        entry_id_counter += 1
        
        return jsonify({
            'message': 'Journal entry added successfully',
            'entry': entry
        }), 201
        
    except Exception as e:
        logger.error(f"Error adding journal entry: {e}")
        return jsonify({'error': 'Failed to add journal entry'}), 500

@app.route('/journal', methods=['GET'])
def get_journal_entries():
    """Get journal entries"""
    try:
        user_id = request.args.get('user_id', 'user123')
        limit = int(request.args.get('limit', 10))
        
        user_entries = [entry for entry in journal_entries if entry['user_id'] == user_id]
        user_entries.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return jsonify(user_entries[:limit])
        
    except Exception as e:
        logger.error(f"Error getting journal entries: {e}")
        return jsonify({'error': 'Failed to get journal entries'}), 500

@app.route('/analytics/summary', methods=['GET'])
def get_analytics_summary():
    """Get analytics summary"""
    try:
        user_id = request.args.get('user_id', 'user123')
        
        user_entries = [entry for entry in journal_entries if entry['user_id'] == user_id]
        
        if not user_entries:
            return jsonify({
                'total_entries': 0,
                'emotion_distribution': {},
                'average_confidence': 0,
                'most_common_emotion': 'none',
                'recent_emotion': 'none'
            })
        
        # Calculate statistics
        emotions = [entry['emotion'] for entry in user_entries]
        confidences = [entry['confidence'] for entry in user_entries]
        
        emotion_counts = Counter(emotions)
        most_common_emotion = emotion_counts.most_common(1)[0][0] if emotion_counts else 'none'
        recent_emotion = user_entries[0]['emotion'] if user_entries else 'none'
        
        summary = {
            'total_entries': len(user_entries),
            'emotion_distribution': dict(emotion_counts),
            'average_confidence': np.mean(confidences),
            'most_common_emotion': most_common_emotion,
            'recent_emotion': recent_emotion
        }
        
        return jsonify(summary)
        
    except Exception as e:
        logger.error(f"Error getting analytics summary: {e}")
        return jsonify({'error': 'Failed to get analytics summary'}), 500

@app.route('/analytics/timeline', methods=['GET'])
def get_timeline():
    """Get timeline data"""
    try:
        user_id = request.args.get('user_id', 'user123')
        limit = int(request.args.get('limit', 30))
        
        user_entries = [entry for entry in journal_entries if entry['user_id'] == user_id]
        user_entries.sort(key=lambda x: x['timestamp'], reverse=True)
        
        timeline = []
        for entry in user_entries[:limit]:
            timeline.append({
                'id': entry['id'],
                'date': entry['timestamp'][:10],  # Just the date part
                'emotion': entry['emotion'],
                'confidence': entry['confidence'],
                'text': entry['text']
            })
        
        return jsonify({
            'timeline': timeline,
            'count': len(timeline)
        })
        
    except Exception as e:
        logger.error(f"Error getting timeline: {e}")
        return jsonify({'error': 'Failed to get timeline'}), 500

@app.route('/ai/insights', methods=['POST'])
def get_ai_insights_endpoint():
    """Get AI-generated insights"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Analytics data is required'}), 400
        
        insights = get_ai_insights(data)
        
        return jsonify({
            'insights': insights
        })
        
    except Exception as e:
        logger.error(f"Error generating AI insights: {e}")
        return jsonify({'error': 'Failed to generate insights'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True) 