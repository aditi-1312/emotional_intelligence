from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import json
import os
from datetime import datetime
from typing import Dict, List, Any
import logging

from config import Config, config, DATA_DIR, MODELS_DIR, WELLNESS_FILE
from models import EmotionModelManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(config['default'])

# Configure CORS
CORS(app, origins=app.config['CORS_ORIGINS'], supports_credentials=True)

# Initialize model manager
try:
    model_manager = EmotionModelManager(
        models_dir=str(MODELS_DIR),
        data_dir=str(DATA_DIR)
    )
    logger.info("Model manager initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize model manager: {e}")
    model_manager = None

# Load wellness suggestions
def load_wellness_suggestions() -> Dict:
    """Load wellness suggestions from JSON file."""
    try:
        with open(WELLNESS_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading wellness suggestions: {e}")
        return {"categories": []}

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'models_loaded': model_manager is not None
    })

# Root endpoint
@app.route('/', methods=['GET'])
def root():
    """Root endpoint with API information."""
    return jsonify({
        'message': 'Emotional Intelligence API',
        'version': '1.0.0',
        'endpoints': {
            'health': '/health',
            'analyze': '/analyze',
            'journal': '/journal',
            'analytics': '/analytics/summary',
            'timeline': '/analytics/timeline',
            'suggestions': '/suggestions',
            'insights': '/ai/insights'
        }
    })

# Emotion analysis endpoint
@app.route('/analyze', methods=['POST'])
def analyze_emotion():
    """Analyze emotion in text."""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'Text is required'}), 400
        
        text = data['text']
        model_name = data.get('model', 'logistic_regression')
        
        if not text.strip():
            return jsonify({'error': 'Text cannot be empty'}), 400
        
        if not model_manager:
            return jsonify({'error': 'Model manager not available'}), 503
        
        # Analyze emotion
        analysis = model_manager.predict_emotion(text, model_name)
        
        return jsonify({
            'success': True,
            'analysis': analysis,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in emotion analysis: {e}")
        return jsonify({'error': str(e)}), 500

# Journal endpoints
@app.route('/journal', methods=['GET', 'POST'])
def journal_entries():
    """Handle journal entries."""
    try:
        if not model_manager:
            return jsonify({'error': 'Model manager not available'}), 503
        
        if request.method == 'POST':
            # Add new journal entry
            data = request.get_json()
            
            if not data or 'text' not in data:
                return jsonify({'error': 'Text is required'}), 400
            
            text = data['text']
            user_id = data.get('user_id', 'default')
            
            if not text.strip():
                return jsonify({'error': 'Text cannot be empty'}), 400
            
            # Add entry with emotion analysis
            entry = model_manager.add_journal_entry(text, user_id)
            
            return jsonify({
                'success': True,
                'entry': entry,
                'message': 'Journal entry added successfully'
            }), 201
        
        else:
            # Get journal entries
            user_id = request.args.get('user_id', 'default')
            limit = request.args.get('limit', type=int)
            
            entries = model_manager.get_journal_entries(user_id, limit if limit is not None else None)
            
            return jsonify({
                'success': True,
                'entries': entries,
                'count': len(entries)
            })
    
    except Exception as e:
        logger.error(f"Error in journal operations: {e}")
        return jsonify({'error': str(e)}), 500

# Analytics endpoints
@app.route('/analytics/summary', methods=['GET'])
def analytics_summary():
    """Get analytics summary."""
    try:
        if not model_manager:
            return jsonify({'error': 'Model manager not available'}), 503
        
        user_id = request.args.get('user_id', 'default')
        summary = model_manager.get_analytics_summary(user_id)
        
        return jsonify({
            'success': True,
            'summary': summary
        })
    
    except Exception as e:
        logger.error(f"Error getting analytics summary: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/analytics/timeline', methods=['GET'])
def analytics_timeline():
    """Get timeline data."""
    try:
        if not model_manager:
            return jsonify({'error': 'Model manager not available'}), 503
        
        user_id = request.args.get('user_id', 'default')
        limit = request.args.get('limit', 30, type=int)
        
        timeline = model_manager.get_timeline_data(user_id, limit)
        
        return jsonify({
            'success': True,
            'timeline': timeline,
            'count': len(timeline)
        })
    
    except Exception as e:
        logger.error(f"Error getting timeline data: {e}")
        return jsonify({'error': str(e)}), 500

# Wellness suggestions endpoint
@app.route('/suggestions', methods=['GET'])
def get_suggestions():
    """Get wellness suggestions."""
    try:
        suggestions = load_wellness_suggestions()
        
        # Get user's recent emotion for personalized suggestions
        user_id = request.args.get('user_id', 'default')
        emotion = request.args.get('emotion', 'neutral')
        
        if model_manager:
            entries = model_manager.get_journal_entries(user_id, 1)
            if entries:
                emotion = entries[-1]['dominant_emotion']
        
        # Add personalized suggestions based on emotion
        personalized = {
            'anger': [
                "Take deep breaths and count to 10",
                "Go for a walk to release tension",
                "Practice progressive muscle relaxation",
                "Write down your feelings in a journal",
                "Listen to calming music"
            ],
            'sadness': [
                "Reach out to a friend or family member",
                "Do something you enjoy",
                "Practice self-compassion",
                "Get some fresh air and sunlight",
                "Try a new hobby or activity"
            ],
            'fear': [
                "Practice grounding techniques",
                "Focus on what you can control",
                "Talk to someone you trust",
                "Use positive affirmations",
                "Take small steps toward your goals"
            ],
            'joy': [
                "Share your happiness with others",
                "Express gratitude for this moment",
                "Do something kind for someone else",
                "Capture this feeling in a journal",
                "Celebrate your positive emotions"
            ],
            'love': [
                "Express your feelings to loved ones",
                "Spend quality time with people you care about",
                "Practice acts of kindness",
                "Write a letter to someone special",
                "Create something beautiful"
            ],
            'surprise': [
                "Take time to process this new information",
                "Stay open to new possibilities",
                "Ask questions to understand better",
                "Embrace the unexpected",
                "Share your surprise with others"
            ],
            'neutral': [
                "Take a moment to check in with yourself",
                "Try something new today",
                "Practice mindfulness",
                "Set a small goal for the day",
                "Connect with nature"
            ]
        }
        
        # Add personalized suggestions to the response
        suggestions['personalized'] = personalized.get(emotion, personalized['neutral'])
        suggestions['current_emotion'] = emotion
        
        return jsonify({
            'success': True,
            'suggestions': suggestions
        })
    
    except Exception as e:
        logger.error(f"Error getting suggestions: {e}")
        return jsonify({'error': str(e)}), 500

# AI insights endpoint
@app.route('/ai/insights', methods=['GET'])
def get_insights():
    """Get AI-powered emotional insights."""
    try:
        if not model_manager:
            return jsonify({'error': 'Model manager not available'}), 503
        
        user_id = request.args.get('user_id', 'default')
        insights = model_manager.get_emotion_insights(user_id)
        
        return jsonify({
            'success': True,
            'insights': insights
        })
    
    except Exception as e:
        logger.error(f"Error getting insights: {e}")
        return jsonify({'error': str(e)}), 500

# Model performance endpoint
@app.route('/models/performance', methods=['GET'])
def get_model_performance():
    """Get model performance metrics."""
    try:
        if not model_manager:
            return jsonify({'error': 'Model manager not available'}), 503
        
        performance = model_manager.get_model_performance()
        
        return jsonify({
            'success': True,
            'performance': performance
        })
    
    except Exception as e:
        logger.error(f"Error getting model performance: {e}")
        return jsonify({'error': str(e)}), 500

# Demo endpoints for testing
@app.route('/auth/demo', methods=['GET'])
def auth_demo():
    """Demo authentication endpoint."""
    return jsonify({
        'success': True,
        'user': {
            'id': 'demo_user',
            'name': 'Demo User',
            'email': 'demo@example.com'
        }
    })

@app.route('/auth/user', methods=['GET'])
def get_user():
    """Get current user information."""
    return jsonify({
        'success': True,
        'user': {
            'id': 'demo_user',
            'name': 'Demo User',
            'email': 'demo@example.com',
            'is_authenticated': True
        }
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

if __name__ == '__main__':
    # Run the Flask app
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    ) 