#!/usr/bin/env python3
"""
Flask API for Emotional Intelligence Analysis
Provides RESTful endpoints for emotion analysis with Google OAuth authentication
"""

from flask import Flask, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from oauthlib.oauth2 import WebApplicationClient
import requests
import sqlite3
import pandas as pd
import numpy as np
import os
import sys
import joblib
from datetime import datetime
import logging
from collections import Counter
import json
import ssl
import certifi

# Add backend/src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import from src directory explicitly to avoid conflicts
from src.data_processor import AdvancedTextProcessor
from src.models import AdvancedEmotionAnalyzer
from src.utils import DataUtils

# Load environment variables
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'config.env'))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')

# Enable CORS
CORS(app, supports_credentials=True)

# Google OAuth Configuration
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

# Google OAuth endpoints (direct URLs instead of discovery)
GOOGLE_AUTH_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_ENDPOINT = "https://www.googleapis.com/oauth2/v2/userinfo"

# OAuth 2.0 client setup
if GOOGLE_CLIENT_ID:
    client = WebApplicationClient(GOOGLE_CLIENT_ID)
else:
    client = None
    logger.warning("Google OAuth not configured - GOOGLE_CLIENT_ID not set")

# SSL Certificate handling for macOS
ssl_context = ssl.create_default_context(cafile=certifi.where())
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Create a session with SSL configuration
requests_session = requests.Session()
requests_session.verify = certifi.where()

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)

# Database setup
def init_db():
    """Initialize the database with users and journal entries tables"""
    # Get the absolute path to the project root
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    instance_dir = os.path.join(project_root, 'data_and_models', 'instance')
    
    # Create instance directory if it doesn't exist
    os.makedirs(instance_dir, exist_ok=True)
    
    db_path = os.path.join(instance_dir, 'emotional_intelligence.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            google_id TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            picture TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create journal entries table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS journal_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            text TEXT NOT NULL,
            emotion TEXT NOT NULL,
            confidence REAL NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    logger.info("Database tables created")

# Initialize database
init_db()

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, id, google_id, email, name, picture):
        self.id = id
        self.google_id = google_id
        self.email = email
        self.name = name
        self.picture = picture

def get_db_connection():
    """Get database connection with correct path"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    db_path = os.path.join(project_root, 'data_and_models', 'instance', 'emotional_intelligence.db')
    return sqlite3.connect(db_path)

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    
    if user_data:
        return User(user_data[0], user_data[1], user_data[2], user_data[3], user_data[4])
    return None

def get_user_by_google_id(google_id):
    """Get user by Google ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE google_id = ?', (google_id,))
    user_data = cursor.fetchone()
    conn.close()
    
    if user_data:
        return User(user_data[0], user_data[1], user_data[2], user_data[3], user_data[4])
    return None

def create_user(google_id, email, name, picture):
    """Create a new user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO users (google_id, email, name, picture) VALUES (?, ?, ?, ?)',
        (google_id, email, name, picture)
    )
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return User(user_id, google_id, email, name, picture)

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
        
        # Get recent journal entries for context from database
        recent_entries = []
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT text, dominant_emotion, timestamp FROM journal_entries WHERE user_id = ? ORDER BY timestamp DESC LIMIT 3',
            (current_user.id,)
        )
        db_entries = cursor.fetchall()
        conn.close()
        
        # Format recent entries
        for entry in db_entries:
            recent_entries.append({
                'text': entry[0][:200] + '...' if len(entry[0]) > 200 else entry[0],
                'emotion': entry[1],
                'date': entry[2][:10]
            })
        
        # Create a more detailed and personalized prompt
        prompt = (
            "\n"
            "You are a compassionate, empathetic mental health companion. Based on this person's mood tracking data, provide personalized, warm, and supportive insights.\n\n"
            "**Their Journey So Far:**\n"
            "- They've been journaling for {days} days\n"
            "- Their most frequent emotion: {most_common_emotion}\n"
            "- Their current mood: {current_mood}\n"
            "- Their emotional clarity: {average_confidence:.1%}\n"
            "- Their emotional landscape: {emotion_distribution}\n\n"
            "**Recent Reflections:**\n"
            "{recent_reflections}\n\n"
            "**Please provide:**\n"
            "1. **A warm, personal reflection** on their emotional journey\n"
            "2. **Specific insights** about their patterns and what they might mean\n"
            "3. **Gentle, actionable suggestions** tailored to their current state\n"
            "4. **Words of encouragement** that feel like they're coming from a caring friend\n"
            "5. **When to consider professional support** (if relevant)\n\n"
            "**Tone Guidelines:**\n"
            "- Be warm, personal, and conversational\n"
            "- Use \"you\" and speak directly to them\n"
            "- Acknowledge their feelings as valid\n"
            "- Offer hope and encouragement\n"
            "- Be specific about their situation, not generic advice\n"
            "- Use emojis sparingly but warmly\n"
            "- Keep it under 300 words\n\n"
            "Remember: You're speaking to someone who's been brave enough to track their emotions. Honor that courage with genuine care and understanding.\n"
        ).format(
            days=analytics_data['total_entries'],
            most_common_emotion=analytics_data['most_common_emotion'],
            current_mood=analytics_data['current_mood'],
            average_confidence=analytics_data['average_confidence'],
            emotion_distribution=analytics_data['emotion_distribution'],
            recent_reflections="\n".join([
                "• {date}: {emotion} - \"{text}\"".format(
                    date=entry['date'],
                    emotion=entry['emotion'],
                    text=entry['text']
                ) for entry in recent_entries
            ])
        )
        
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
    current_mood = analytics_data['current_mood']
    avg_confidence = analytics_data['average_confidence']
    emotion_dist = analytics_data['emotion_distribution']
    
    # Get recent entries for context from database
    recent_text = "your recent reflections"
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT text FROM journal_entries WHERE user_id = ? ORDER BY timestamp DESC LIMIT 1',
        (current_user.id,)
    )
    recent_entry = cursor.fetchone()
    conn.close()
    
    if recent_entry:
        recent_text = recent_entry[0][:100] + '...' if len(recent_entry[0]) > 100 else recent_entry[0]
    
    insights = "I've been following your emotional journey through " + str(total_entries) + " journal entries, and I want to share some personal reflections with you.\n\n"
    
    # Personalized emotion analysis
    if most_common == 'joy':
        insights += "🌟 I've noticed joy has been a constant companion in your life lately. That's beautiful! Your recent entry about \"" + recent_text + "\" shows this positive energy. When joy flows naturally like this, it often means you're aligned with what truly matters to you. Consider what's been fueling this happiness - maybe it's certain activities, people, or moments of achievement?\n\n"
    elif most_common == 'sadness':
        insights += "💙 I see sadness has been present in your journey. Your recent reflection about \"" + recent_text + "\" touches on this. Remember, feeling sad doesn't mean you're doing anything wrong - it's a natural part of being human. Sometimes sadness is our heart's way of processing change or loss. What would feel most supportive to you right now?\n\n"
    elif most_common == 'anger':
        insights += "🔥 Anger has been showing up in your entries, including your recent thoughts about \"" + recent_text + "\". Anger often signals that something important to you feels threatened or unfair. It can be a powerful catalyst for change when channeled mindfully. What might your anger be trying to tell you about your needs or boundaries?\n\n"
    elif most_common == 'fear':
        insights += "😰 I've noticed fear and anxiety appearing in your reflections, like in your recent entry about \"" + recent_text + "\". These feelings are incredibly common and often arise when we're facing uncertainty or change. Your brain is trying to protect you, even if it feels overwhelming. What small steps could help you feel more grounded?\n\n"
    elif most_common == 'surprise':
        insights += "😲 Your emotional landscape has been full of surprises! Your recent reflection about \"" + recent_text + "\" captures this sense of the unexpected. Life has been throwing you curveballs, and you're navigating them with curiosity. This adaptability is a real strength - you're learning to dance with uncertainty.\n\n"
    elif most_common == 'disgust':
        insights += "🤢 I see disgust has been present in your journey, including your recent thoughts about \"" + recent_text + "\". This emotion often arises when something feels fundamentally wrong or out of alignment with your values. It might be signaling that certain aspects of your life need attention or change.\n\n"
    elif most_common == 'love':
        insights += "❤️ Love has been flowing through your entries! Your recent reflection about \"" + recent_text + "\" radiates this warmth. When love is your dominant emotion, it often means you're deeply connected to what matters most. This connection is precious - how can you nurture it further?\n\n"
    elif most_common == 'neutral':
        insights += "😐 I've noticed you've been in a more neutral space lately, including your recent entry about \"" + recent_text + "\". Sometimes this calm center is exactly what we need - a place to rest and reset. It can also be a sign that you're processing deeper emotions beneath the surface.\n\n"
    
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
    
    if current_mood in ['sadness', 'fear']:
        insights += "• Try a simple grounding exercise: name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, 1 you can taste\n"
        insights += "• Reach out to someone you trust - even a brief connection can help\n"
        insights += "• Give yourself permission to rest and be gentle with yourself\n"
    elif current_mood == 'joy':
        insights += "• Savor these positive moments - maybe take a mental snapshot\n"
        insights += "• Consider what's working well and how you can create more of it\n"
        insights += "• Share your good energy with someone who might need it\n"
    elif current_mood == 'anger':
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

def get_analytics_data(user_id):
    """Get analytics data for a specific user"""
    try:
        # Get user's journal entries from database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT dominant_emotion, confidence, timestamp FROM journal_entries WHERE user_id = ? ORDER BY timestamp DESC',
            (user_id,)
        )
        entries = cursor.fetchall()
        conn.close()
        
        if not entries:
            return {
                'total_entries': 0,
                'most_common_emotion': 'No data',
                'emotion_distribution': {},
                'average_confidence': 0,
                'current_mood': 'No data'
            }
        
        # Process analytics
        emotions = [entry[0] for entry in entries]
        confidences = [entry[1] for entry in entries]
        
        emotion_counts = Counter(emotions)
        most_common_emotion = emotion_counts.most_common(1)[0][0] if emotion_counts else 'No data'
        
        # Get current mood (most recent entry)
        current_mood = emotions[0] if emotions else 'No data'
        
        return {
            'total_entries': len(entries),
            'most_common_emotion': most_common_emotion,
            'emotion_distribution': dict(emotion_counts),
            'average_confidence': round(sum(confidences) / len(confidences), 2),
            'current_mood': current_mood
        }
        
    except Exception as e:
        logger.error(f"Error getting analytics data: {e}")
        return {
            'total_entries': 0,
            'most_common_emotion': 'Error',
            'emotion_distribution': {},
            'average_confidence': 0,
            'current_mood': 'Error'
        }

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
@login_required
def add_journal_entry():
    """Add a new journal entry for the authenticated user"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        # Analyze the text
        analysis = analyzer.analyze_text(text)
        dominant_emotion = analysis['dominant_emotion']
        confidence = analysis['confidence']
        
        # Store in database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO journal_entries (user_id, text, dominant_emotion, confidence, timestamp) VALUES (?, ?, ?, ?, ?)',
            (current_user.id, text, dominant_emotion, confidence, datetime.now().isoformat())
        )
        entry_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Also store in memory for backward compatibility
        global entry_id_counter
        entry = {
            'id': entry_id_counter,
            'user_id': current_user.id,
            'text': text,
            'dominant_emotion': dominant_emotion,
            'confidence': confidence,
            'timestamp': datetime.now().isoformat()
        }
        journal_entries.append(entry)
        entry_id_counter += 1
        
        return jsonify({
            'id': entry_id,
            'text': text,
            'dominant_emotion': dominant_emotion,
            'confidence': confidence,
            'timestamp': entry['timestamp']
        }), 201
        
    except Exception as e:
        logger.error(f"Error adding journal entry: {e}")
        return jsonify({'error': 'Failed to add journal entry'}), 500

@app.route('/journal', methods=['GET'])
@login_required
def get_journal_entries():
    """Get journal entries for the authenticated user"""
    try:
        limit = request.args.get('limit', 10, type=int)
        
        # Get from database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT id, text, dominant_emotion, confidence, timestamp FROM journal_entries WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?',
            (current_user.id, limit)
        )
        entries = cursor.fetchall()
        conn.close()
        
        # Format entries
        formatted_entries = []
        for entry in entries:
            formatted_entries.append({
                'id': entry[0],
                'text': entry[1],
                'dominant_emotion': entry[2],
                'confidence': entry[3],
                'timestamp': entry[4]
            })
        
        return jsonify(formatted_entries)
        
    except Exception as e:
        logger.error(f"Error getting journal entries: {e}")
        return jsonify({'error': 'Failed to get journal entries'}), 500

@app.route('/analytics/summary', methods=['GET'])
@login_required
def get_analytics_summary():
    """Get analytics summary for the authenticated user"""
    try:
        # Get user's journal entries from database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT dominant_emotion, confidence, timestamp FROM journal_entries WHERE user_id = ? ORDER BY timestamp DESC',
            (current_user.id,)
        )
        entries = cursor.fetchall()
        conn.close()
        
        if not entries:
            return jsonify({
                'total_entries': 0,
                'most_common_emotion': 'No data',
                'emotion_distribution': {},
                'average_confidence': 0,
                'current_mood': 'No data'
            })
        
        # Process analytics
        emotions = [entry[0] for entry in entries]
        confidences = [entry[1] for entry in entries]
        
        emotion_counts = Counter(emotions)
        most_common_emotion = emotion_counts.most_common(1)[0][0] if emotion_counts else 'No data'
        
        # Get current mood (most recent entry)
        current_mood = emotions[0] if emotions else 'No data'
        
        analytics = {
            'total_entries': len(entries),
            'most_common_emotion': most_common_emotion,
            'emotion_distribution': dict(emotion_counts),
            'average_confidence': round(sum(confidences) / len(confidences), 2),
            'current_mood': current_mood
        }
        
        return jsonify(analytics)
        
    except Exception as e:
        logger.error(f"Error getting analytics summary: {e}")
        return jsonify({'error': 'Failed to get analytics summary'}), 500

@app.route('/analytics/timeline', methods=['GET'])
@login_required
def get_timeline():
    """Get timeline data for the authenticated user"""
    try:
        # Get user's journal entries from database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT text, dominant_emotion, confidence, timestamp FROM journal_entries WHERE user_id = ? ORDER BY timestamp DESC LIMIT 30',
            (current_user.id,)
        )
        entries = cursor.fetchall()
        conn.close()
        
        # Format timeline data
        timeline = []
        for entry in entries:
            timeline.append({
                'text': entry[0],
                'dominant_emotion': entry[1],
                'confidence': entry[2],
                'timestamp': entry[3]
            })
        
        return jsonify(timeline)
        
    except Exception as e:
        logger.error(f"Error getting timeline: {e}")
        return jsonify({'error': 'Failed to get timeline'}), 500

@app.route('/ai/insights', methods=['POST'])
@login_required
def get_ai_insights_endpoint():
    """Get AI insights for user's mood data"""
    try:
        # Get analytics data for the authenticated user
        analytics_data = get_analytics_data(current_user.id)
        
        # Generate insights
        insights = get_ai_insights(analytics_data)
        
        return jsonify(insights)
    except Exception as e:
        logger.error(f"Error getting AI insights: {e}")
        return jsonify({'error': 'Failed to generate insights'}), 500

@app.route('/suggestions', methods=['GET'])
def get_suggestions():
    """Get general mental health and wellness suggestions"""
    try:
        suggestions = {
            'categories': [
                {
                    'title': '🌅 Morning Wellness',
                    'suggestions': [
                        'Start your day with 5-10 minutes of deep breathing or meditation',
                        'Write down 3 things you\'re grateful for',
                        'Take a few minutes to stretch and move your body',
                        'Eat a nourishing breakfast to fuel your day',
                        'Set one small, achievable goal for the day'
                    ]
                },
                {
                    'title': '💪 Stress Management',
                    'suggestions': [
                        'Practice the 4-7-8 breathing technique: inhale 4, hold 7, exhale 8',
                        'Take regular breaks during work - try the Pomodoro technique',
                        'Go for a short walk in nature when feeling overwhelmed',
                        'Listen to calming music or nature sounds',
                        'Practice progressive muscle relaxation'
                    ]
                },
                {
                    'title': '😴 Sleep Hygiene',
                    'suggestions': [
                        'Create a consistent bedtime routine',
                        'Avoid screens 1 hour before bed',
                        'Keep your bedroom cool, dark, and quiet',
                        'Try reading a book or journaling before sleep',
                        'Avoid caffeine after 2 PM'
                    ]
                },
                {
                    'title': '🤝 Social Connection',
                    'suggestions': [
                        'Reach out to a friend or family member today',
                        'Join a club or group that interests you',
                        'Practice active listening in conversations',
                        'Share your feelings with someone you trust',
                        'Plan a small gathering or coffee meetup'
                    ]
                },
                {
                    'title': '🎯 Personal Growth',
                    'suggestions': [
                        'Learn something new - take an online course or read a book',
                        'Set aside time for hobbies you enjoy',
                        'Practice self-compassion and positive self-talk',
                        'Keep a gratitude journal',
                        'Try a new activity or skill'
                    ]
                },
                {
                    'title': '🧘‍♀️ Mindfulness & Relaxation',
                    'suggestions': [
                        'Practice mindful eating - savor each bite',
                        'Take a mindful walk, noticing your surroundings',
                        'Try guided meditation apps',
                        'Practice yoga or gentle stretching',
                        'Spend time in nature without distractions'
                    ]
                },
                {
                    'title': '🏃‍♀️ Physical Wellness',
                    'suggestions': [
                        'Find a form of exercise you enjoy',
                        'Take the stairs instead of the elevator',
                        'Dance to your favorite music',
                        'Try a new sport or physical activity',
                        'Take regular movement breaks throughout the day'
                    ]
                },
                {
                    'title': '💡 Creative Expression',
                    'suggestions': [
                        'Write in a journal about your thoughts and feelings',
                        'Try drawing, painting, or coloring',
                        'Learn to play a musical instrument',
                        'Take photos of things that bring you joy',
                        'Write poetry or short stories'
                    ]
                }
            ]
        }
        
        return jsonify(suggestions)
    except Exception as e:
        logger.error(f"Error getting suggestions: {e}")
        return jsonify({'error': 'Failed to get suggestions'}), 500

@app.route('/journal/clear', methods=['DELETE'])
@login_required
def clear_journal_entries():
    """Clear all journal entries for the current user"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Delete all journal entries for the current user
        cursor.execute('DELETE FROM journal_entries WHERE user_id = ?', (current_user.id,))
        deleted_count = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        logger.info(f"Cleared {deleted_count} journal entries for user {current_user.id}")
        
        return jsonify({
            'message': f'Successfully cleared {deleted_count} journal entries',
            'deleted_count': deleted_count
        })
    except Exception as e:
        logger.error(f"Error clearing journal entries: {e}")
        return jsonify({'error': 'Failed to clear journal entries'}), 500

# Google OAuth Authentication Routes
@app.route('/auth/login')
def login():
    """Initiate Google OAuth login"""
    if not client:
        return jsonify({'error': 'Google OAuth not configured. Please set GOOGLE_CLIENT_ID in config.env'}), 500
    
    try:
        # Use direct Google OAuth endpoints with proper flow configuration
        request_uri = client.prepare_request_uri(
            GOOGLE_AUTH_ENDPOINT,
            redirect_uri='http://localhost:5001/auth/callback',
            scope=["openid", "email", "profile"],
            state='emotional_intelligence_app',  # Add state parameter for security
            access_type='offline',  # Request refresh token
            prompt='consent'  # Always show consent screen
        )
        return redirect(request_uri)
    except Exception as e:
        logger.error(f"Error in Google OAuth login: {e}")
        return jsonify({'error': 'An unexpected error occurred during login setup'}), 500

@app.route('/auth/callback')
def callback():
    """Handle Google OAuth callback"""
    if not client:
        return jsonify({'error': 'Google OAuth not configured'}), 500
    
    try:
        # Get authorization code and state from Google
        code = request.args.get("code")
        state = request.args.get("state")
        error = request.args.get("error")
        
        # Check for OAuth errors
        if error:
            logger.error(f"Google OAuth error: {error}")
            return jsonify({'error': f'Google OAuth error: {error}'}), 400
        
        if not code:
            return jsonify({'error': 'No authorization code received'}), 400
        
        # Verify state parameter for security
        if state != 'emotional_intelligence_app':
            logger.warning(f"State mismatch: expected 'emotional_intelligence_app', got '{state}'")
        
        # Prepare and send a request to get tokens using direct endpoint
        token_url, headers, body = client.prepare_token_request(
            GOOGLE_TOKEN_ENDPOINT,
            authorization_response=request.url,
            redirect_url='http://localhost:5001/auth/callback',
            code=code
        )
        token_response = requests_session.post(
            token_url,
            headers=headers,
            data=body,
            auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET) if GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET else None,
            timeout=10
        )
        token_response.raise_for_status()
        
        # Parse the tokens!
        client.parse_request_body_response(json.dumps(token_response.json()))
        
        # Now get user info using direct endpoint
        uri, headers, body = client.add_token(GOOGLE_USERINFO_ENDPOINT)
        userinfo_response = requests_session.get(uri, headers=headers, data=body, timeout=10)
        userinfo_response.raise_for_status()
        
        userinfo = userinfo_response.json()
        
        # You want to make sure their email is verified.
        # The user authenticated with Google, authorized your
        # app, and now you've verified their email through Google!
        if userinfo.get("verified_email", True):  # Google API v2 doesn't always include this field
            unique_id = userinfo["id"]
            users_email = userinfo["email"]
            users_name = userinfo["name"]
            users_picture = userinfo.get("picture", "")
        else:
            return "User email not available or not verified by Google.", 400
        
        # Check if user exists in database
        user = get_user_by_google_id(unique_id)
        if not user:
            # Create new user
            user = create_user(unique_id, users_email, users_name, users_picture)
        
        # Begin user session by logging the user in
        login_user(user)
        
        # Redirect to frontend with success parameter
        return redirect('http://localhost:3000?auth=success')
        
    except requests.exceptions.SSLError as e:
        logger.error(f"SSL Error in Google OAuth callback: {e}")
        return jsonify({'error': 'SSL certificate error during authentication.'}), 500
    except requests.exceptions.RequestException as e:
        logger.error(f"Error in Google OAuth callback: {e}")
        return jsonify({'error': 'Unable to complete Google OAuth. Please try again.'}), 500
    except (KeyError, ValueError) as e:
        logger.error(f"Error parsing Google OAuth response: {e}")
        return jsonify({'error': 'Invalid response from Google OAuth'}), 500
    except Exception as e:
        logger.error(f"Unexpected error in Google OAuth callback: {e}")
        return jsonify({'error': 'An unexpected error occurred during login'}), 500

@app.route('/auth/logout')
@login_required
def logout():
    """Logout user"""
    logout_user()
    return redirect('http://localhost:3000')

@app.route('/auth/demo')
def demo_login():
    """Demo login for testing without Google OAuth"""
    try:
        # Check if demo user exists in database, if not create it
        existing_user = get_user_by_google_id("demo_user")
        if existing_user:
            demo_user = existing_user
        else:
            # Create a demo user with a better avatar
            demo_user = create_user(
                "demo_user", 
                "demo@example.com", 
                "Demo User", 
                "demo"  # Use "demo" as a special identifier for demo avatar
            )
        
        # Begin user session
        login_user(demo_user)
        
        return jsonify({
            'message': 'Demo login successful',
            'user': {
                'id': demo_user.id,
                'email': demo_user.email,
                'name': demo_user.name,
                'picture': demo_user.picture
            }
        })
    except Exception as e:
        logger.error(f"Error in demo login: {e}")
        return jsonify({'error': 'Demo login failed'}), 500

@app.route('/auth/user')
def get_user():
    """Get current user information"""
    if current_user.is_authenticated:
        return jsonify({
            'id': current_user.id,
            'email': current_user.email,
            'name': current_user.name,
            'picture': current_user.picture
        })
    else:
        return jsonify({'error': 'Not authenticated'}), 401

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True) 