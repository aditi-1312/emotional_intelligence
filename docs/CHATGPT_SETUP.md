# ChatGPT Integration Setup

This guide explains how to enable ChatGPT-powered insights in your mood tracker application.

## Features Added

1. **Insightful Quotes**: The Dashboard now displays motivational quotes related to your mood
2. **Advice Page**: After 5 journal entries, users can access personalized advice
3. **Professional Resources**: Links to mental health professionals and crisis support
4. **AI-Powered Insights**: ChatGPT integration for personalized mood analysis
5. **Self-Care Tips**: Practical suggestions for emotional well-being

## ChatGPT Integration

### Option 1: Use ChatGPT API (Recommended)

1. **Get an OpenAI API Key**:
   - Visit [OpenAI Platform](https://platform.openai.com/)
   - Create an account or sign in
   - Go to "API Keys" section
   - Create a new API key

2. **Add API Key to Environment**:
   ```bash
   # Add to your config.env file
   OPENAI_API_KEY=your_api_key_here
   ```

3. **Benefits**:
   - Personalized insights based on your mood patterns
   - Professional mental health advice
   - Contextual recommendations
   - Natural language explanations

### Option 2: Use Rule-Based Insights (Default)

If you don't have an OpenAI API key, the application will automatically use rule-based insights that provide:
- Analysis of your most common emotions
- Personalized advice based on mood patterns
- Self-care suggestions
- Professional help recommendations

## How It Works

### Dashboard Features

1. **Quote Display**: Shows motivational quotes based on your most common emotion
2. **Advice Notification**: Appears after 5 entries, encouraging you to visit the Advice page
3. **Current Mood**: Displays your most recent journal entry with emotion analysis

### Advice Page Features

1. **AI Insights**: Personalized analysis of your mood patterns
2. **Professional Resources**: Links to therapists, crisis support, and mental health apps
3. **Self-Care Tips**: Practical suggestions for emotional well-being
4. **Warning Signs**: Information about when to seek professional help

## API Endpoints

- `POST /ai/insights` - Generate AI-powered insights from mood data
- `GET /analytics/summary` - Get mood analytics summary
- `GET /analytics/timeline` - Get mood timeline data
- `POST /journal` - Add new journal entry
- `GET /journal` - Get journal entries

## Mental Health Resources Included

### Crisis Support
- **National Suicide Prevention Lifeline**: 988
- **Crisis Text Line**: Text HOME to 741741

### Professional Help
- **Psychology Today**: Find therapists and psychiatrists
- **BetterHelp**: Online therapy platform
- **Talkspace**: Online therapy and psychiatry

### Wellness Resources
- **Mindful.org**: Mindfulness and meditation
- **Headspace**: Meditation app

## Privacy and Security

- All journal entries are stored locally (in-memory for demo)
- ChatGPT API calls only send anonymized mood statistics
- No personal journal text is sent to external services
- Professional resources are external links to trusted organizations

## Getting Started

1. **Start the API**:
   ```bash
   PORT=5001 python3 api.py
   ```

2. **Start the Frontend**:
   ```bash
   cd frontend
   npm start
   ```

3. **Add Journal Entries**: Write at least 5 entries to unlock the Advice page

4. **Visit the Advice Page**: Click the "🧠 Advice" link in the navigation

## Customization

### Adding More Quotes
Edit the `QUOTES` object in `frontend/src/components/Dashboard.tsx` to add more motivational quotes.

### Adding More Resources
Edit the `mentalHealthResources` array in `frontend/src/components/Advice.tsx` to add more professional resources.

### Customizing AI Prompts
Modify the `get_chatgpt_insights` function in `api.py` to customize the AI analysis prompts.

## Troubleshooting

### ChatGPT API Issues
- Check your API key is correct
- Ensure you have sufficient API credits
- Verify internet connectivity
- The app will fallback to rule-based insights if ChatGPT is unavailable

### Frontend Issues
- Clear browser cache
- Check console for JavaScript errors
- Ensure the API is running on port 5001

### API Issues
- Check the API logs for error messages
- Verify all dependencies are installed
- Ensure port 5001 is available

## Support

For technical issues:
1. Check the console logs
2. Verify all dependencies are installed
3. Ensure the API and frontend are running
4. Check network connectivity

For mental health support:
- Contact the resources listed in the Advice page
- Reach out to a mental health professional
- Use crisis support services if needed

Remember: This application is for educational and self-reflection purposes. It is not a substitute for professional mental health care. 