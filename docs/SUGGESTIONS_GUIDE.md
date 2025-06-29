# Wellness Suggestions Guide

This guide explains how to use the wellness suggestions feature in the Emotional Intelligence app and how to programmatically fetch all suggestions.

## 🌟 Overview

The wellness suggestions feature provides users with gentle, actionable mental health and wellness recommendations organized into 8 categories:

1. **🌅 Morning Wellness** - Start your day right
2. **💪 Stress Management** - Cope with stress effectively
3. **😴 Sleep Hygiene** - Improve your sleep quality
4. **🤝 Social Connection** - Build meaningful relationships
5. **🎯 Personal Growth** - Develop yourself
6. **🧘‍♀️ Mindfulness & Relaxation** - Find inner peace
7. **🏃‍♀️ Physical Wellness** - Take care of your body
8. **💡 Creative Expression** - Express yourself creatively

## 🚀 How to Access Suggestions

### 1. Through the Web App

1. **Login** to the Emotional Intelligence app
2. **Navigate** to the "Advice" section
3. **Scroll down** to the "💡 Wellness Suggestions" section
4. **Browse** through different categories
5. **Choose** suggestions that resonate with you

### 2. Through the API

#### Endpoint
```
GET /suggestions
```

#### Example Response
```json
{
  "categories": [
    {
      "title": "🌅 Morning Wellness",
      "suggestions": [
        "Start your day with 5-10 minutes of deep breathing or meditation",
        "Write down 3 things you're grateful for",
        "Take a few minutes to stretch and move your body",
        "Eat a nourishing breakfast to fuel your day",
        "Set one small, achievable goal for the day"
      ]
    }
  ]
}
```

## 🔧 Programmatic Access

### Python Example

```python
import requests

def fetch_suggestions():
    response = requests.get("http://localhost:5001/suggestions")
    return response.json()

# Get all suggestions
suggestions = fetch_suggestions()

# Print all categories
for category in suggestions['categories']:
    print(f"{category['title']}:")
    for suggestion in category['suggestions']:
        print(f"  - {suggestion}")
```

### JavaScript/Node.js Example

```javascript
const fetch = require('node-fetch');

async function fetchSuggestions() {
    const response = await fetch('http://localhost:5001/suggestions');
    return response.json();
}

// Get all suggestions
const suggestions = await fetchSuggestions();

// Print all categories
suggestions.categories.forEach(category => {
    console.log(`${category.title}:`);
    category.suggestions.forEach(suggestion => {
        console.log(`  - ${suggestion}`);
    });
});
```

### Frontend React Example

```typescript
import { apiService } from '../services/api';

const fetchSuggestions = async () => {
    try {
        const response = await apiService.getSuggestions();
        return response.data;
    } catch (error) {
        console.error('Error fetching suggestions:', error);
        return null;
    }
};

// Usage in component
const [suggestions, setSuggestions] = useState(null);

useEffect(() => {
    const loadSuggestions = async () => {
        const data = await fetchSuggestions();
        setSuggestions(data);
    };
    loadSuggestions();
}, []);
```

## 📊 Available Scripts

### 1. Python Script (`scripts/fetch_suggestions.py`)

Run with:
```bash
python3 scripts/fetch_suggestions.py
```

Features:
- Fetches all suggestions from the API
- Prints them in a formatted way
- Shows total categories and suggestions count
- Demonstrates filtering by category
- Provides random suggestion functionality
- Saves suggestions to JSON file

### 2. JavaScript Script (`scripts/fetch_suggestions.js`)

Run with:
```bash
node scripts/fetch_suggestions.js
```

Features:
- Same functionality as Python script
- Additional emotion-based filtering
- Node.js compatible
- Can be used as a module in other projects

## 🎯 Advanced Usage

### Filtering by Category

```python
def get_suggestions_by_category(suggestions, category_title):
    for category in suggestions['categories']:
        if category['title'] == category_title:
            return category['suggestions']
    return []

# Usage
stress_suggestions = get_suggestions_by_category(suggestions, "💪 Stress Management")
```

### Getting Random Suggestions

```python
import random

def get_random_suggestion(suggestions):
    all_suggestions = []
    for category in suggestions['categories']:
        all_suggestions.extend(category['suggestions'])
    
    if all_suggestions:
        return random.choice(all_suggestions)
    return "No suggestions available."
```

### Emotion-Based Filtering (JavaScript)

```javascript
function getSuggestionsByEmotion(suggestions, emotion) {
    const emotionMap = {
        'sadness': ['🤝 Social Connection', '💡 Creative Expression'],
        'anger': ['💪 Stress Management', '🧘‍♀️ Mindfulness & Relaxation'],
        'joy': ['🎯 Personal Growth', '💡 Creative Expression'],
        // ... more emotions
    };
    
    const relevantCategories = emotionMap[emotion] || [];
    const relevantSuggestions = [];
    
    relevantCategories.forEach(categoryTitle => {
        const categorySuggestions = getSuggestionsByCategory(suggestions, categoryTitle);
        relevantSuggestions.push(...categorySuggestions);
    });
    
    return relevantSuggestions;
}
```

## 📝 Data Structure

### Suggestion Category
```typescript
interface SuggestionCategory {
    title: string;        // Category title with emoji
    suggestions: string[]; // Array of suggestion strings
}
```

### Suggestions Response
```typescript
interface Suggestions {
    categories: SuggestionCategory[];
}
```

## 🔄 Adding New Suggestions

To add new suggestions, edit the `get_suggestions()` function in `backend/api.py`:

```python
@app.route('/suggestions', methods=['GET'])
def get_suggestions():
    suggestions = {
        'categories': [
            {
                'title': '🌅 Morning Wellness',
                'suggestions': [
                    'Your new suggestion here',
                    'Another suggestion',
                    # ... more suggestions
                ]
            },
            # ... more categories
        ]
    }
    return jsonify(suggestions)
```

## 🎨 Customization

### Frontend Styling

The suggestions section uses CSS classes defined in `frontend/src/components/Advice.css`:

- `.suggestions-grid` - Grid layout for categories
- `.suggestion-category` - Individual category cards
- `.suggestion-item` - Individual suggestion items
- `.suggestions-footer` - Footer message

### Backend Configuration

You can modify the suggestions by:
1. Adding new categories
2. Adding new suggestions to existing categories
3. Reordering categories
4. Customizing suggestion content

## 🚨 Error Handling

The API includes proper error handling:

```python
try:
    # Fetch suggestions logic
    return jsonify(suggestions)
except Exception as e:
    logger.error(f"Error getting suggestions: {e}")
    return jsonify({'error': 'Failed to get suggestions'}), 500
```

## 📈 Statistics

Current suggestion statistics:
- **Total Categories**: 8
- **Total Suggestions**: 40
- **Average per Category**: 5 suggestions
- **Categories**: Morning Wellness, Stress Management, Sleep Hygiene, Social Connection, Personal Growth, Mindfulness & Relaxation, Physical Wellness, Creative Expression

## 🤝 Contributing

To contribute new suggestions:

1. **Fork** the repository
2. **Add** your suggestions to the appropriate category in `backend/api.py`
3. **Test** the changes locally
4. **Submit** a pull request

## 📞 Support

If you have questions about the suggestions feature:

1. Check this documentation
2. Review the example scripts
3. Test the API endpoint directly
4. Open an issue on GitHub

---

**Remember**: These are gentle suggestions, not prescriptions. Choose what feels right for you, and be kind to yourself in the process. 💝 