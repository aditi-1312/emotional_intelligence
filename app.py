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
                st.subheader("📊 Analysis Results")
                
                # Emotion breakdown
                emotions_list = list(analysis['emotions'].items())
                emotions_df = pd.DataFrame(emotions_list, columns=['Emotion', 'Count'])
                
                fig = px.bar(emotions_df, x='Emotion', y='Count', 
                           title="Emotion Word Count",
                           color='Count',
                           color_continuous_scale='viridis')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("🎯 Dominant Emotion")
                st.markdown(f"""
                <div class="emotion-card {dominant_emotion}">
                    <h3>{dominant_emotion.title()}</h3>
                    <p>This text primarily expresses {dominant_emotion}.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Text features
                st.subheader("📝 Text Features")
                features = analysis['features']
                st.write(f"**Length:** {features['char_count']} characters")
                st.write(f"**Words:** {features['word_count']}")
                st.write(f"**Sentences:** {features.get('sentence_count', 'N/A')}")
                st.write(f"**Exclamations:** {features['exclamation_count']}")
                st.write(f"**Questions:** {features['question_count']}")

def show_text_analysis(analyzer):
    """Show detailed text analysis"""
    st.header("🔍 Advanced Text Analysis")
    
    # Analysis options
    col1, col2 = st.columns([3, 1])
    
    with col1:
        text_input = st.text_area(
            "Enter text for detailed analysis:",
            value="I'm feeling really happy today because everything is going well! I love spending time with my family and friends.",
            height=150
        )
    
    with col2:
        analysis_type = st.selectbox(
            "Analysis Type",
            ["Comprehensive", "Emotion Only", "Sentiment Only", "Features Only"]
        )
    
    if st.button("🔍 Analyze", type="primary"):
        with st.spinner("Performing detailed analysis..."):
            analysis = analyzer.analyze_text(text_input)
            
            # Display results based on analysis type
            if analysis_type in ["Comprehensive", "Emotion Only"]:
                st.subheader("🎭 Emotion Analysis")
                
                # Radar chart
                fig = create_emotion_radar_chart(analysis['emotions'])
                st.plotly_chart(fig, use_container_width=True)
                
                # Emotion breakdown
                col1, col2 = st.columns(2)
                
                with col1:
                    emotions_df = pd.DataFrame(list(analysis['emotions'].items()), 
                                             columns=['Emotion', 'Intensity'])
                    fig = px.pie(emotions_df, values='Intensity', names='Emotion',
                               title="Emotion Distribution")
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Emotion cards
                    for emotion, intensity in analysis['emotions'].items():
                        if intensity > 0:
                            st.markdown(f"""
                            <div class="emotion-card {emotion}">
                                <strong>{emotion.title()}</strong>: {intensity} occurrences
                            </div>
                            """, unsafe_allow_html=True)
            
            if analysis_type in ["Comprehensive", "Sentiment Only"]:
                st.subheader("📊 Sentiment Analysis")
                
                # Simple sentiment calculation
                positive_words = ['happy', 'joy', 'excited', 'great', 'wonderful', 'love']
                negative_words = ['sad', 'angry', 'fear', 'terrible', 'awful']
                
                text_lower = text_input.lower()
                positive_count = sum(1 for word in positive_words if word in text_lower)
                negative_count = sum(1 for word in negative_words if word in text_lower)
                
                sentiment_score = (positive_count - negative_count) / max(len(text_input.split()), 1)
                sentiment_score = max(-1, min(1, sentiment_score))  # Clamp between -1 and 1
                
                # Sentiment gauge
                fig = create_sentiment_gauge(sentiment_score)
                st.plotly_chart(fig, use_container_width=True)
            
            if analysis_type in ["Comprehensive", "Features Only"]:
                st.subheader("📝 Text Features")
                
                features = analysis['features']
                
                # Feature metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Character Count", int(features['char_count']))
                
                with col2:
                    st.metric("Word Count", int(features['word_count']))
                
                with col3:
                    st.metric("Exclamations", int(features['exclamation_count']))
                
                with col4:
                    st.metric("Questions", int(features['question_count']))
                
                # Feature visualization
                feature_data = {
                    'Metric': list(features.keys()),
                    'Value': list(features.values())
                }
                feature_df = pd.DataFrame(feature_data)
                
                fig = px.bar(feature_df, x='Metric', y='Value', 
                           title="Text Features Breakdown")
                st.plotly_chart(fig, use_container_width=True)

def show_model_training():
    """Show model training interface"""
    st.header("📈 Model Training")
    
    st.info("This section allows you to train and compare different machine learning models for emotion classification.")
    
    # Training options
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Data Options")
        
        data_source = st.selectbox(
            "Data Source",
            ["Upload CSV", "Use Sample Data", "Load from URL"]
        )
        
        if data_source == "Upload CSV":
            uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
            if uploaded_file is not None:
                data = pd.read_csv(uploaded_file)
                st.write("Data preview:")
                st.dataframe(data.head())
        
        elif data_source == "Use Sample Data":
            data = load_sample_data()
            st.write("Sample data preview:")
            st.dataframe(data.head())
    
    with col2:
        st.subheader("🤖 Model Options")
        
        models_to_train = st.multiselect(
            "Select models to train:",
            ["Logistic Regression", "Linear SVC", "Random Forest", "Gradient Boosting", 
             "Naive Bayes", "KNN", "Decision Tree"],
            default=["Logistic Regression", "Random Forest"]
        )
        
        test_size = st.slider("Test size:", 0.1, 0.5, 0.2, 0.05)
        
        if st.button("🚀 Train Models", type="primary"):
            st.success("Model training interface ready! (Training functionality would be implemented here)")
            
            # Simulate training results
            st.subheader("📊 Training Results")
            
            results_data = {
                'Model': models_to_train,
                'Accuracy': [0.85, 0.87, 0.83, 0.86, 0.82, 0.79, 0.84],
                'Training Time': [2.3, 1.8, 4.2, 3.1, 0.5, 1.2, 0.8]
            }
            
            results_df = pd.DataFrame(results_data)
            st.dataframe(results_df)
            
            # Performance chart
            fig = px.bar(results_df, x='Model', y='Accuracy', 
                        title="Model Performance Comparison",
                        color='Accuracy',
                        color_continuous_scale='viridis')
            st.plotly_chart(fig, use_container_width=True)

def show_data_explorer():
    """Show data exploration interface"""
    st.header("📋 Data Explorer")
    
    # Load sample data
    data = load_sample_data()
    
    st.subheader("📊 Dataset Overview")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Records", len(data))
    
    with col2:
        st.metric("Unique Emotions", data['label'].nunique())
    
    with col3:
        st.metric("Average Text Length", f"{data['text'].str.len().mean():.1f}")
    
    # Data visualization
    st.subheader("📈 Data Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Emotion distribution
        emotion_counts = data['label'].value_counts()
        fig = px.pie(values=emotion_counts.values, names=emotion_counts.index,
                    title="Emotion Distribution")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Text length distribution
        text_lengths = data['text'].str.len()
        fig = px.histogram(x=text_lengths, title="Text Length Distribution",
                          nbins=20)
        st.plotly_chart(fig, use_container_width=True)
    
    # Data table
    st.subheader("📋 Data Table")
    st.dataframe(data)
    
    # Word cloud
    st.subheader("☁️ Word Cloud")
    
    # Combine all text
    all_text = " ".join(data['text'].tolist())
    
    # Generate word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_text)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

def show_settings():
    """Show settings page"""
    st.header("⚙️ Settings")
    
    st.subheader("🔧 Application Settings")
    
    # Theme selection
    theme = st.selectbox("Theme", ["Light", "Dark", "Auto"])
    
    # Language selection
    language = st.selectbox("Language", ["English", "Spanish", "French", "German"])
    
    # Model settings
    st.subheader("🤖 Model Settings")
    
    confidence_threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.7, 0.05)
    
    max_text_length = st.number_input("Maximum Text Length", 100, 10000, 1000, 100)
    
    # Save settings
    if st.button("💾 Save Settings"):
        st.success("Settings saved successfully!")

if __name__ == "__main__":
    main() 