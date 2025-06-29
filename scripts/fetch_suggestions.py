#!/usr/bin/env python3
"""
Script to fetch all wellness suggestions from the Emotional Intelligence API.
This demonstrates how to programmatically access all suggestions.
"""

import requests
import json
from typing import Dict, List

def fetch_all_suggestions(api_url: str = "http://localhost:5001") -> Dict:
    """
    Fetch all wellness suggestions from the API.
    
    Args:
        api_url: The base URL of the API (default: http://localhost:5001)
    
    Returns:
        Dictionary containing all suggestion categories and their suggestions
    """
    try:
        response = requests.get(f"{api_url}/suggestions")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching suggestions: {e}")
        return {}

def print_suggestions(suggestions: Dict):
    """
    Print all suggestions in a formatted way.
    
    Args:
        suggestions: Dictionary containing suggestion categories
    """
    if not suggestions or 'categories' not in suggestions:
        print("No suggestions found or invalid response format.")
        return
    
    print("🌟 Wellness Suggestions 🌟")
    print("=" * 50)
    
    for category in suggestions['categories']:
        print(f"\n{category['title']}")
        print("-" * len(category['title']))
        
        for i, suggestion in enumerate(category['suggestions'], 1):
            print(f"{i}. {suggestion}")
    
    print(f"\n📊 Total Categories: {len(suggestions['categories'])}")
    total_suggestions = sum(len(cat['suggestions']) for cat in suggestions['categories'])
    print(f"📝 Total Suggestions: {total_suggestions}")

def get_suggestions_by_category(suggestions: Dict, category_title: str) -> List[str]:
    """
    Get suggestions for a specific category.
    
    Args:
        suggestions: Dictionary containing suggestion categories
        category_title: Title of the category to filter by
    
    Returns:
        List of suggestions for the specified category
    """
    for category in suggestions.get('categories', []):
        if category['title'] == category_title:
            return category['suggestions']
    return []

def get_random_suggestion(suggestions: Dict) -> str:
    """
    Get a random suggestion from any category.
    
    Args:
        suggestions: Dictionary containing suggestion categories
    
    Returns:
        A random suggestion string
    """
    import random
    
    all_suggestions = []
    for category in suggestions.get('categories', []):
        all_suggestions.extend(category['suggestions'])
    
    if all_suggestions:
        return random.choice(all_suggestions)
    return "No suggestions available."

def main():
    """Main function to demonstrate fetching and using suggestions."""
    print("🔍 Fetching wellness suggestions from the API...")
    
    # Fetch all suggestions
    suggestions = fetch_all_suggestions()
    
    if not suggestions:
        print("❌ Failed to fetch suggestions. Make sure the API is running.")
        return
    
    # Print all suggestions
    print_suggestions(suggestions)
    
    # Example: Get suggestions for a specific category
    print("\n" + "=" * 50)
    print("🎯 Example: Stress Management Suggestions")
    print("=" * 50)
    stress_suggestions = get_suggestions_by_category(suggestions, "💪 Stress Management")
    for i, suggestion in enumerate(stress_suggestions, 1):
        print(f"{i}. {suggestion}")
    
    # Example: Get a random suggestion
    print("\n" + "=" * 50)
    print("🎲 Random Suggestion of the Day")
    print("=" * 50)
    random_suggestion = get_random_suggestion(suggestions)
    print(f"💡 {random_suggestion}")
    
    # Example: Save suggestions to a JSON file
    print("\n" + "=" * 50)
    print("💾 Saving suggestions to file...")
    try:
        with open('wellness_suggestions.json', 'w') as f:
            json.dump(suggestions, f, indent=2)
        print("✅ Suggestions saved to 'wellness_suggestions.json'")
    except Exception as e:
        print(f"❌ Error saving suggestions: {e}")

if __name__ == "__main__":
    main() 