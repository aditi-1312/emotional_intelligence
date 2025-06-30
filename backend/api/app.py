import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import joblib
import os
import sys
from datetime import datetime

# Add src to path
sys.path.append('src')

from src.data_processor import AdvancedTextProcessor, FeatureExtractor
from src.models import EmotionClassifier, AdvancedEmotionAnalyzer

# Page configuration
st.set_page_config(
    page_title="Emotional Intelligence Analyzer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .emotion-card {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .joy { background-color: #ffeb3b; }
    .sadness { background-color: #2196f3; }
    .anger { background-color: #f44336; }
    .fear { background-color: #9c27b0; }
    .surprise { background-color: #ff9800; }
    .love { background-color: #e91e63; }
    .neutral { background-color: #9e9e9e; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_sample_data():
    """Load sample data for demonstration"""
    # Create sample data
    sample_texts = [
        "I'm feeling so happy today! Everything is going great!",
        "I'm really sad and depressed about what happened yesterday.",
        "I'm absolutely furious about this situation!",
        "I'm scared and anxious about the upcoming exam.",
        "Wow! I'm so surprised by this amazing news!",
        "I love spending time with my family and friends.",
        "The weather is nice today.",
        "I'm feeling quite neutral about this decision.",
        "This makes me so angry and frustrated!",
        "I'm delighted to see you again!"
    ]
    
    sample_emotions = ['joy', 'sadness', 'anger', 'fear', 'surprise', 'love', 'neutral', 'neutral', 'anger', 'joy']
    
    return pd.DataFrame({
        'text': sample_texts,
        'label': sample_emotions
    })

@st.cache_resource
def initialize_analyzer():
    """Initialize the emotion analyzer"""
    return AdvancedEmotionAnalyzer()

def create_emotion_radar_chart(emotions):
    """Create radar chart for emotions"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=list(emotions.values()),
        theta=list(emotions.keys()),
        fill='toself',
        name='Emotion Intensity',
        line_color='rgb(32, 201, 151)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(emotions.values()) + 1]
            )),
        showlegend=False,
        title="Emotion Analysis Radar Chart"
    )
    
    return fig

def create_sentiment_gauge(sentiment_score):
    """Create gauge chart for sentiment"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = sentiment_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Sentiment Score"},
        delta = {'reference': 0},
        gauge = {
            'axis': {'range': [-1, 1]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [-1, -0.5], 'color': "lightgray"},
                {'range': [-0.5, 0], 'color': "gray"},
                {'range': [0, 0.5], 'color': "lightgreen"},
                {'range': [0.5, 1], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 0
            }
        }
    ))
    
    return fig

def main():
    """Main application"""
    
    # Header
    st.markdown('<h1 class="main-header">🧠 Emotional Intelligence Analyzer</h1>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page",
        ["📊 Dashboard", "🔍 Text Analysis", "📈 Model Training", "📋 Data Explorer", "⚙️ Settings"]
    )
    
    # Initialize analyzer
    analyzer = initialize_analyzer()
    
    if page == "📊 Dashboard":
        show_dashboard(analyzer)
    elif page == "🔍 Text Analysis":
        show_text_analysis(analyzer)
    elif page == "📈 Model Training":
        show_model_training()
    elif page == "📋 Data Explorer":
        show_data_explorer()
    elif page == "⚙️ Settings":
        show_settings()

def show_dashboard(analyzer):
    """Show the main dashboard"""
    st.header("📊 Emotional Intelligence Dashboard")
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Analyses", "1,234", "+12%")
    
    with col2:
        st.metric("Accuracy", "87.5%", "+2.3%")
    
    with col3:
        st.metric("Most Common Emotion", "Joy", "32%")
    
    with col4:
        st.metric("Active Models", "8", "2 new")
    
    # Sample analysis
    st.subheader("🎯 Quick Analysis")
    
    sample_text = st.text_area(
        "Enter text to analyze:",
        value="I'm feeling really happy today because everything is going well!",
        height=100
    )
    
    if st.button("Analyze Emotion"):
        with st.spinner("Analyzing..."):
            analysis = analyzer.analyze_text(sample_text)
            dominant_emotion = analyzer.get_dominant_emotion(analysis)
            
            # Display results
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader("Analysis Results")
                
                # Emotion breakdown
                emotions = analysis.get('emotions', {})
                if emotions:
                    st.write("**Emotion Scores:**")
                    for emotion, score in emotions.items():
                        st.progress(score)
                        st.write(f"{emotion.capitalize()}: {score:.3f}")
                
                # Dominant emotion
                if dominant_emotion:
                    st.success(f"**Dominant Emotion:** {dominant_emotion.capitalize()}")
                
                # Confidence
                confidence = analysis.get('confidence', 0)
                st.info(f"**Confidence:** {confidence:.2%}")
            
            with col2:
                # Radar chart
                if emotions:
                    fig = create_emotion_radar_chart(emotions)
                    st.plotly_chart(fig, use_container_width=True)
    
    # Recent activity
    st.subheader("📈 Recent Activity")
    
    # Sample activity data
    activity_data = pd.DataFrame({
        'Date': pd.date_range(start='2024-01-01', periods=7, freq='D'),
        'Analyses': [45, 52, 38, 67, 43, 58, 49],
        'Avg Confidence': [0.85, 0.87, 0.82, 0.89, 0.84, 0.86, 0.88]
    })
    
    fig = px.line(activity_data, x='Date', y='Analyses', title='Daily Analyses')
    st.plotly_chart(fig, use_container_width=True)

def show_text_analysis(analyzer):
    """Show text analysis page"""
    st.header("🔍 Text Analysis")
    
    # Text input
    text_input = st.text_area(
        "Enter text to analyze:",
        height=150,
        placeholder="Type or paste your text here..."
    )
    
    if st.button("Analyze", type="primary"):
        if text_input.strip():
            with st.spinner("Analyzing text..."):
                # Perform analysis
                analysis = analyzer.analyze_text(text_input)
                dominant_emotion = analyzer.get_dominant_emotion(analysis)
                
                # Display results
                st.subheader("📊 Analysis Results")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Emotion scores
                    emotions = analysis.get('emotions', {})
                    if emotions:
                        st.write("**Emotion Distribution:**")
                        emotion_df = pd.DataFrame(list(emotions.items()), columns=['Emotion', 'Score'])
                        fig = px.bar(emotion_df, x='Emotion', y='Score', title='Emotion Scores')
                        st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Dominant emotion
                    if dominant_emotion:
                        st.success(f"**Dominant Emotion:** {dominant_emotion.capitalize()}")
                    
                    # Confidence
                    confidence = analysis.get('confidence', 0)
                    st.info(f"**Confidence:** {confidence:.2%}")
                    
                    # Sentiment
                    sentiment = analysis.get('sentiment', 0)
                    st.metric("Sentiment Score", f"{sentiment:.3f}")
                
                # Detailed analysis
                st.subheader("🔍 Detailed Analysis")
                
                # Text features
                features = analysis.get('features', {})
                if features:
                    st.write("**Text Features:**")
                    for feature, value in features.items():
                        st.write(f"- {feature}: {value}")
                
                # Cleaned text
                cleaned_text = analysis.get('cleaned_text', '')
                if cleaned_text:
                    st.write("**Processed Text:**")
                    st.code(cleaned_text)
        else:
            st.warning("Please enter some text to analyze.")

def show_model_training():
    """Show model training page"""
    st.header("📈 Model Training")
    
    st.write("This page allows you to train and manage emotion analysis models.")
    
    # Training options
    st.subheader("Training Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Available Models:**")
        models = [
            "Logistic Regression",
            "Random Forest", 
            "Gradient Boosting",
            "Support Vector Machine",
            "Naive Bayes"
        ]
        
        for model in models:
            st.write(f"- {model}")
    
    with col2:
        st.write("**Training Parameters:**")
        st.write("- Test Size: 20%")
        st.write("- Random State: 42")
        st.write("- Cross Validation: 5-fold")
    
    # Training button
    if st.button("Start Training", type="primary"):
        with st.spinner("Training models..."):
            # Simulate training
            import time
            time.sleep(2)
            
            st.success("Training completed!")
            st.write("Models have been trained and saved successfully.")

def show_data_explorer():
    """Show data explorer page"""
    st.header("📋 Data Explorer")
    
    # Load sample data
    data = load_sample_data()
    
    st.subheader("Sample Dataset")
    st.dataframe(data)
    
    # Data statistics
    st.subheader("Dataset Statistics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Total Samples:** {len(data)}")
        st.write(f"**Unique Emotions:** {data['label'].nunique()}")
    
    with col2:
        st.write(f"**Average Text Length:** {data['text'].str.len().mean():.1f} characters")
        st.write(f"**Longest Text:** {data['text'].str.len().max()} characters")
    
    # Emotion distribution
    st.subheader("Emotion Distribution")
    emotion_counts = data['label'].value_counts()
    fig = px.pie(values=emotion_counts.values, names=emotion_counts.index, title='Emotion Distribution')
    st.plotly_chart(fig, use_container_width=True)
    
    # Text length distribution
    st.subheader("Text Length Distribution")
    data['text_length'] = data['text'].str.len()
    fig = px.histogram(data, x='text_length', title='Text Length Distribution')
    st.plotly_chart(fig, use_container_width=True)

def show_settings():
    """Show settings page"""
    st.header("⚙️ Settings")
    
    st.write("Configure your Emotional Intelligence Analyzer settings.")
    
    # Model settings
    st.subheader("Model Settings")
    
    confidence_threshold = st.slider(
        "Confidence Threshold",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.1,
        help="Minimum confidence level for emotion predictions"
    )
    
    max_text_length = st.number_input(
        "Maximum Text Length",
        min_value=100,
        max_value=10000,
        value=1000,
        step=100,
        help="Maximum number of characters to process"
    )
    
    # Display settings
    st.subheader("Display Settings")
    
    theme = st.selectbox(
        "Theme",
        ["Light", "Dark"],
        help="Choose the application theme"
    )
    
    show_confidence = st.checkbox(
        "Show Confidence Scores",
        value=True,
        help="Display confidence scores in analysis results"
    )
    
    # Save settings
    if st.button("Save Settings", type="primary"):
        st.success("Settings saved successfully!")

if __name__ == "__main__":
    main()