#!/usr/bin/env python3
"""
🧠 Emotional Intelligence Analyzer - Streamlit Dashboard
=======================================================

A comprehensive dashboard for analyzing emotions, testing ML models,
and visualizing emotional patterns.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import requests
from datetime import datetime, timedelta
import time
from typing import Dict, List, Any

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
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .emotion-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        margin: 0.5rem 0;
    }
    .positive { border-left: 4px solid #2ecc71; }
    .negative { border-left: 4px solid #e74c3c; }
    .neutral { border-left: 4px solid #95a5a6; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'api_base_url' not in st.session_state:
    st.session_state.api_base_url = "http://localhost:5001"

if 'test_entries' not in st.session_state:
    st.session_state.test_entries = []

# API helper functions
def make_api_request(endpoint: str, method: str = "GET", data: Dict = None) -> Dict:
    """Make API request to the backend."""
    try:
        url = f"{st.session_state.api_base_url}{endpoint}"
        
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        else:
            return {"error": f"Unsupported method: {method}"}
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API Error: {response.status_code} - {response.text}"}
    
    except requests.exceptions.RequestException as e:
        return {"error": f"Connection Error: {str(e)}"}

def check_api_health() -> bool:
    """Check if the API is running."""
    result = make_api_request("/health")
    return "error" not in result

# Main dashboard
def main():
    """Main dashboard function."""
    
    # Header
    st.markdown('<h1 class="main-header">🧠 Emotional Intelligence Analyzer</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Configuration")
        
        # API URL configuration
        api_url = st.text_input(
            "API Base URL",
            value=st.session_state.api_base_url,
            help="URL of the Flask API backend"
        )
        
        if st.button("Update API URL"):
            st.session_state.api_base_url = api_url
            st.success("API URL updated!")
        
        # Health check
        if check_api_health():
            st.success("✅ API Connected")
        else:
            st.error("❌ API Not Connected")
            st.info("Make sure the Flask API is running on the specified URL")
        
        st.divider()
        
        # Navigation
        st.header("📊 Navigation")
        page = st.selectbox(
            "Choose a page",
            ["🏠 Dashboard", "📝 Journal", "📈 Analytics", "🤖 Model Testing", "💡 Insights", "⚙️ Settings"]
        )
    
    # Page routing
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "📝 Journal":
        show_journal()
    elif page == "📈 Analytics":
        show_analytics()
    elif page == "🤖 Model Testing":
        show_model_testing()
    elif page == "💡 Insights":
        show_insights()
    elif page == "⚙️ Settings":
        show_settings()

def show_dashboard():
    """Show the main dashboard."""
    st.header("🏠 Dashboard Overview")
    
    # Check API health
    if not check_api_health():
        st.error("❌ Cannot connect to API. Please check if the backend is running.")
        return
    
    # Get analytics summary
    summary = make_api_request("/analytics/summary")
    
    if "error" in summary:
        st.error(f"Error loading analytics: {summary['error']}")
        return
    
    summary_data = summary.get("summary", {})
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Entries",
            summary_data.get("total_entries", 0),
            help="Total number of journal entries"
        )
    
    with col2:
        st.metric(
            "Current Mood",
            summary_data.get("current_mood", "neutral").title(),
            help="Overall mood based on recent entries"
        )
    
    with col3:
        st.metric(
            "Most Common Emotion",
            summary_data.get("most_common_emotion", "neutral").title(),
            help="Most frequently detected emotion"
        )
    
    with col4:
        st.metric(
            "Average Confidence",
            f"{summary_data.get('average_confidence', 0):.2f}",
            help="Average confidence of emotion predictions"
        )
    
    # Emotion distribution chart
    st.subheader("📊 Emotion Distribution")
    
    emotion_dist = summary_data.get("emotion_distribution", {})
    if emotion_dist:
        # Create pie chart
        fig = px.pie(
            values=list(emotion_dist.values()),
            names=list(emotion_dist.keys()),
            title="Distribution of Emotions",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No emotion data available. Add some journal entries to see the distribution.")
    
    # Recent activity
    st.subheader("📅 Recent Activity")
    
    timeline = make_api_request("/analytics/timeline?limit=10")
    if "error" not in timeline:
        timeline_data = timeline.get("timeline", [])
        
        if timeline_data:
            # Create timeline chart
            df_timeline = pd.DataFrame(timeline_data)
            df_timeline['timestamp'] = pd.to_datetime(df_timeline['timestamp'])
            
            fig = px.scatter(
                df_timeline,
                x='timestamp',
                y='sentiment_score',
                color='emotion',
                size='confidence',
                hover_data=['text'],
                title="Recent Journal Entries Timeline",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_layout(xaxis_title="Time", yaxis_title="Sentiment Score")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No recent entries. Start journaling to see your timeline!")
    else:
        st.error(f"Error loading timeline: {timeline['error']}")

def show_journal():
    """Show the journal page."""
    st.header("📝 Journal")
    
    # Check API health
    if not check_api_health():
        st.error("❌ Cannot connect to API. Please check if the backend is running.")
        return
    
    # Add new entry
    st.subheader("✍️ Add New Entry")
    
    with st.form("journal_entry"):
        entry_text = st.text_area(
            "How are you feeling today?",
            placeholder="Describe your emotions, thoughts, or experiences...",
            height=150
        )
        
        col1, col2 = st.columns(2)
        with col1:
            model_choice = st.selectbox(
                "ML Model",
                ["logistic_regression", "random_forest", "gradient_boosting", "linear_svc", "naive_bayes"],
                help="Choose the ML model for emotion analysis"
            )
        
        with col2:
            user_id = st.text_input("User ID", value="demo_user", help="User identifier")
        
        submitted = st.form_submit_button("📝 Save Entry")
        
        if submitted and entry_text.strip():
            # Analyze emotion first
            analysis_result = make_api_request("/analyze", "POST", {
                "text": entry_text,
                "model": model_choice
            })
            
            if "error" not in analysis_result:
                # Save to journal
                journal_result = make_api_request("/journal", "POST", {
                    "text": entry_text,
                    "user_id": user_id
                })
                
                if "error" not in journal_result:
                    st.success("✅ Entry saved successfully!")
                    
                    # Show analysis results
                    analysis = analysis_result.get("analysis", {})
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Emotion", analysis.get("dominant_emotion", "unknown").title())
                    with col2:
                        st.metric("Confidence", f"{analysis.get('confidence', 0):.2f}")
                    with col3:
                        sentiment = analysis_result.get("analysis", {}).get("sentiment_score", 0)
                        st.metric("Sentiment", f"{sentiment:.2f}")
                    
                    # Emotion breakdown
                    emotions = analysis.get("emotions", {})
                    if emotions:
                        st.subheader("🎭 Emotion Breakdown")
                        emotion_df = pd.DataFrame(list(emotions.items()), columns=['Emotion', 'Probability'])
                        emotion_df = emotion_df.sort_values('Probability', ascending=False)
                        
                        fig = px.bar(
                            emotion_df,
                            x='Emotion',
                            y='Probability',
                            title="Emotion Probabilities",
                            color='Probability',
                            color_continuous_scale='viridis'
                        )
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.error(f"Error saving entry: {journal_result['error']}")
            else:
                st.error(f"Error analyzing text: {analysis_result['error']}")
    
    # View entries
    st.subheader("📖 Recent Entries")
    
    entries = make_api_request("/journal")
    if "error" not in entries:
        entries_data = entries.get("entries", [])
        
        if entries_data:
            # Display entries in reverse chronological order
            for entry in reversed(entries_data[-10:]):  # Show last 10 entries
                emotion = entry.get("dominant_emotion", "neutral")
                sentiment = entry.get("sentiment_score", 0)
                
                # Determine card class based on sentiment
                card_class = "positive" if sentiment > 0.1 else "negative" if sentiment < -0.1 else "neutral"
                
                st.markdown(f"""
                <div class="emotion-card {card_class}">
                    <strong>📅 {entry.get('timestamp', 'Unknown')}</strong><br>
                    <strong>🎭 {emotion.title()}</strong> (Confidence: {entry.get('confidence', 0):.2f})<br>
                    <strong>💭 {entry.get('text', 'No text')}</strong>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No journal entries yet. Add your first entry above!")
    else:
        st.error(f"Error loading entries: {entries['error']}")

def show_analytics():
    """Show the analytics page."""
    st.header("📈 Analytics")
    
    # Check API health
    if not check_api_health():
        st.error("❌ Cannot connect to API. Please check if the backend is running.")
        return
    
    # Get analytics data
    summary = make_api_request("/analytics/summary")
    timeline = make_api_request("/analytics/timeline?limit=50")
    
    if "error" in summary or "error" in timeline:
        st.error("Error loading analytics data")
        return
    
    summary_data = summary.get("summary", {})
    timeline_data = timeline.get("timeline", [])
    
    # Detailed metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Key Metrics")
        
        metrics = [
            ("Total Entries", summary_data.get("total_entries", 0)),
            ("Entries This Week", summary_data.get("entries_this_week", 0)),
            ("Entries This Month", summary_data.get("entries_this_month", 0)),
            ("Average Confidence", f"{summary_data.get('average_confidence', 0):.2f}"),
            ("Average Sentiment", f"{summary_data.get('average_sentiment', 0):.2f}"),
            ("Sentiment Trend", summary_data.get("sentiment_trend", "unknown").title())
        ]
        
        for label, value in metrics:
            st.metric(label, value)
    
    with col2:
        st.subheader("🎭 Current Status")
        
        status_items = [
            ("Current Mood", summary_data.get("current_mood", "neutral").title()),
            ("Recent Emotion", summary_data.get("recent_emotion", "neutral").title()),
            ("Most Common Emotion", summary_data.get("most_common_emotion", "neutral").title())
        ]
        
        for label, value in status_items:
            st.info(f"**{label}:** {value}")
    
    # Timeline analysis
    if timeline_data:
        st.subheader("📅 Timeline Analysis")
        
        df_timeline = pd.DataFrame(timeline_data)
        df_timeline['timestamp'] = pd.to_datetime(df_timeline['timestamp'])
        df_timeline['date'] = pd.to_datetime(df_timeline['date'])
        
        # Sentiment over time
        fig = px.line(
            df_timeline,
            x='timestamp',
            y='sentiment_score',
            title="Sentiment Over Time",
            markers=True
        )
        fig.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Neutral")
        st.plotly_chart(fig, use_container_width=True)
        
        # Emotion frequency over time
        emotion_counts = df_timeline['emotion'].value_counts()
        fig = px.bar(
            x=emotion_counts.index,
            y=emotion_counts.values,
            title="Emotion Frequency",
            labels={'x': 'Emotion', 'y': 'Count'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Confidence distribution
        fig = px.histogram(
            df_timeline,
            x='confidence',
            title="Confidence Distribution",
            nbins=20
        )
        st.plotly_chart(fig, use_container_width=True)

def show_model_testing():
    """Show the model testing page."""
    st.header("🤖 Model Testing")
    
    # Check API health
    if not check_api_health():
        st.error("❌ Cannot connect to API. Please check if the backend is running.")
        return
    
    # Model performance
    st.subheader("📊 Model Performance")
    
    performance = make_api_request("/models/performance")
    if "error" not in performance:
        perf_data = performance.get("performance", {})
        
        if perf_data and "error" not in perf_data:
            # Create performance comparison
            models = list(perf_data.keys())
            accuracies = [perf_data[model].get("accuracy", 0) for model in models]
            
            fig = px.bar(
                x=models,
                y=accuracies,
                title="Model Accuracy Comparison",
                labels={'x': 'Model', 'y': 'Accuracy'},
                color=accuracies,
                color_continuous_scale='viridis'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Performance table
            st.subheader("📋 Detailed Performance")
            perf_df = pd.DataFrame([
                {
                    'Model': model,
                    'Accuracy': f"{data.get('accuracy', 0):.3f}",
                    'Correct': data.get('correct_predictions', 0),
                    'Total': data.get('total_predictions', 0)
                }
                for model, data in perf_data.items()
            ])
            st.dataframe(perf_df, use_container_width=True)
        else:
            st.warning("No performance data available")
    else:
        st.error(f"Error loading performance data: {performance['error']}")
    
    # Test models with sample texts
    st.subheader("🧪 Test Models")
    
    # Sample texts for testing
    sample_texts = [
        "I'm feeling really happy today! Everything is going great!",
        "I'm so sad and disappointed about what happened.",
        "I'm absolutely furious about this situation!",
        "I'm scared and anxious about the future.",
        "I love spending time with my family.",
        "Wow! I'm so surprised by this news!",
        "The weather is nice today."
    ]
    
    col1, col2 = st.columns(2)
    
    with col1:
        test_text = st.text_area(
            "Enter text to test",
            value=sample_texts[0],
            height=100
        )
        
        model_choice = st.selectbox(
            "Select Model",
            ["logistic_regression", "random_forest", "gradient_boosting", "linear_svc", "naive_bayes"]
        )
        
        if st.button("🔍 Analyze"):
            if test_text.strip():
                result = make_api_request("/analyze", "POST", {
                    "text": test_text,
                    "model": model_choice
                })
                
                if "error" not in result:
                    analysis = result.get("analysis", {})
                    
                    st.success("✅ Analysis complete!")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Emotion", analysis.get("dominant_emotion", "unknown").title())
                    with col2:
                        st.metric("Confidence", f"{analysis.get('confidence', 0):.2f}")
                    with col3:
                        st.metric("Model", model_choice.replace("_", " ").title())
                    
                    # Emotion probabilities
                    emotions = analysis.get("emotions", {})
                    if emotions:
                        emotion_df = pd.DataFrame(list(emotions.items()), columns=['Emotion', 'Probability'])
                        emotion_df = emotion_df.sort_values('Probability', ascending=False)
                        
                        fig = px.bar(
                            emotion_df,
                            x='Emotion',
                            y='Probability',
                            title=f"Emotion Probabilities ({model_choice})",
                            color='Probability',
                            color_continuous_scale='viridis'
                        )
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.error(f"Error: {result['error']}")
    
    with col2:
        st.subheader("📝 Sample Texts")
        st.write("Try these sample texts:")
        
        for i, text in enumerate(sample_texts):
            if st.button(f"Sample {i+1}", key=f"sample_{i}"):
                st.session_state.test_text = text
                st.rerun()

def show_insights():
    """Show the insights page."""
    st.header("💡 AI Insights")
    
    # Check API health
    if not check_api_health():
        st.error("❌ Cannot connect to API. Please check if the backend is running.")
        return
    
    # Get insights
    insights = make_api_request("/ai/insights")
    
    if "error" not in insights:
        insights_data = insights.get("insights", {})
        
        # Display insights
        st.subheader("🧠 Emotional Insights")
        
        insights_list = insights_data.get("insights", [])
        if insights_list:
            for insight in insights_list:
                st.info(f"💡 {insight}")
        else:
            st.info("No insights available yet. Add more journal entries to get personalized insights!")
        
        # Recommendations
        st.subheader("💪 Recommendations")
        
        recommendations = insights_data.get("recommendations", [])
        if recommendations:
            for rec in recommendations:
                st.success(f"✅ {rec}")
        else:
            st.info("No specific recommendations at this time.")
        
        # Patterns
        st.subheader("📊 Emotional Patterns")
        
        patterns = insights_data.get("patterns", {})
        if patterns:
            col1, col2 = st.columns(2)
            
            with col1:
                emotion_dist = patterns.get("emotion_distribution", {})
                if emotion_dist:
                    fig = px.pie(
                        values=list(emotion_dist.values()),
                        names=list(emotion_dist.keys()),
                        title="Your Emotional Patterns"
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                avg_sentiment = patterns.get("average_sentiment", 0)
                total_entries = patterns.get("total_entries", 0)
                
                st.metric("Average Sentiment", f"{avg_sentiment:.2f}")
                st.metric("Total Entries", total_entries)
                
                if avg_sentiment > 0.2:
                    st.success("🌟 You tend to have positive emotions!")
                elif avg_sentiment < -0.2:
                    st.warning("😔 You tend to have negative emotions. Consider talking to someone.")
                else:
                    st.info("😐 You tend to have neutral emotions.")
    else:
        st.error(f"Error loading insights: {insights['error']}")

def show_settings():
    """Show the settings page."""
    st.header("⚙️ Settings")
    
    st.subheader("🔧 API Configuration")
    
    # API URL
    new_api_url = st.text_input(
        "API Base URL",
        value=st.session_state.api_base_url,
        help="URL of the Flask API backend"
    )
    
    if st.button("Save API URL"):
        st.session_state.api_base_url = new_api_url
        st.success("API URL saved!")
    
    # Test connection
    if st.button("Test Connection"):
        if check_api_health():
            st.success("✅ API connection successful!")
        else:
            st.error("❌ API connection failed!")
    
    st.divider()
    
    st.subheader("📊 Data Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Clear Test Data"):
            st.session_state.test_entries = []
            st.success("Test data cleared!")
    
    with col2:
        if st.button("Refresh Data"):
            st.rerun()
    
    st.divider()
    
    st.subheader("ℹ️ About")
    
    st.markdown("""
    **Emotional Intelligence Analyzer v1.0.0**
    
    This application uses machine learning to analyze emotions in text and provide insights into emotional patterns.
    
    **Features:**
    - 📝 Journal entries with emotion analysis
    - 📊 Analytics and visualizations
    - 🤖 Multiple ML model testing
    - 💡 AI-powered insights
    - 📈 Timeline analysis
    
    **Technologies:**
    - Flask API backend
    - Streamlit frontend
    - Scikit-learn ML models
    - TF-IDF vectorization
    - Plotly visualizations
    """)

if __name__ == "__main__":
    main() 