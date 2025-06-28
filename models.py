from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import json

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for authentication and user management"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    picture = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with journal entries
    journal_entries = db.relationship('JournalEntry', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'google_id': self.google_id,
            'email': self.email,
            'name': self.name,
            'picture': self.picture,
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat()
        }

class JournalEntry(db.Model):
    """Journal entry model for storing user journal entries"""
    __tablename__ = 'journal_entries'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Analysis results stored as JSON
    dominant_emotion = db.Column(db.String(50))
    confidence = db.Column(db.Float)
    emotions_json = db.Column(db.Text)  # JSON string of emotion scores
    features_json = db.Column(db.Text)  # JSON string of text features
    cleaned_text = db.Column(db.Text)
    total_emotion_words = db.Column(db.Integer)
    
    def __repr__(self):
        return f'<JournalEntry {self.id} by User {self.user_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'text': self.text,
            'timestamp': self.timestamp.isoformat(),
            'analysis': {
                'dominant_emotion': self.dominant_emotion,
                'confidence': self.confidence,
                'emotions': json.loads(self.emotions_json) if self.emotions_json else {},
                'features': json.loads(self.features_json) if self.features_json else {},
                'cleaned_text': self.cleaned_text,
                'total_emotion_words': self.total_emotion_words
            }
        }
    
    @property
    def emotions(self):
        """Get emotions as dictionary"""
        return json.loads(self.emotions_json) if self.emotions_json else {}
    
    @emotions.setter
    def emotions(self, value):
        """Set emotions as JSON string"""
        self.emotions_json = json.dumps(value)
    
    @property
    def features(self):
        """Get features as dictionary"""
        return json.loads(self.features_json) if self.features_json else {}
    
    @features.setter
    def features(self, value):
        """Set features as JSON string"""
        self.features_json = json.dumps(value) 