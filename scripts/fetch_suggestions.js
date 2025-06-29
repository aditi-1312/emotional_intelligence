#!/usr/bin/env node
/**
 * JavaScript script to fetch all wellness suggestions from the Emotional Intelligence API.
 * This demonstrates how to programmatically access all suggestions using Node.js.
 */

const https = require('https');
const http = require('http');
const fs = require('fs');

/**
 * Fetch all wellness suggestions from the API.
 * @param {string} apiUrl - The base URL of the API (default: http://localhost:5001)
 * @returns {Promise<Object>} Dictionary containing all suggestion categories and their suggestions
 */
async function fetchAllSuggestions(apiUrl = "http://localhost:5001") {
    return new Promise((resolve, reject) => {
        const url = new URL(`${apiUrl}/suggestions`);
        const client = url.protocol === 'https:' ? https : http;
        
        const req = client.get(url, (res) => {
            let data = '';
            
            res.on('data', (chunk) => {
                data += chunk;
            });
            
            res.on('end', () => {
                try {
                    const suggestions = JSON.parse(data);
                    resolve(suggestions);
                } catch (error) {
                    reject(new Error(`Failed to parse JSON: ${error.message}`));
                }
            });
        });
        
        req.on('error', (error) => {
            reject(new Error(`Request failed: ${error.message}`));
        });
        
        req.setTimeout(5000, () => {
            req.destroy();
            reject(new Error('Request timeout'));
        });
    });
}

/**
 * Print all suggestions in a formatted way.
 * @param {Object} suggestions - Dictionary containing suggestion categories
 */
function printSuggestions(suggestions) {
    if (!suggestions || !suggestions.categories) {
        console.log("No suggestions found or invalid response format.");
        return;
    }
    
    console.log("🌟 Wellness Suggestions 🌟");
    console.log("=".repeat(50));
    
    suggestions.categories.forEach(category => {
        console.log(`\n${category.title}`);
        console.log("-".repeat(category.title.length));
        
        category.suggestions.forEach((suggestion, index) => {
            console.log(`${index + 1}. ${suggestion}`);
        });
    });
    
    console.log(`\n📊 Total Categories: ${suggestions.categories.length}`);
    const totalSuggestions = suggestions.categories.reduce((sum, cat) => sum + cat.suggestions.length, 0);
    console.log(`📝 Total Suggestions: ${totalSuggestions}`);
}

/**
 * Get suggestions for a specific category.
 * @param {Object} suggestions - Dictionary containing suggestion categories
 * @param {string} categoryTitle - Title of the category to filter by
 * @returns {Array<string>} List of suggestions for the specified category
 */
function getSuggestionsByCategory(suggestions, categoryTitle) {
    const category = suggestions.categories.find(cat => cat.title === categoryTitle);
    return category ? category.suggestions : [];
}

/**
 * Get a random suggestion from any category.
 * @param {Object} suggestions - Dictionary containing suggestion categories
 * @returns {string} A random suggestion string
 */
function getRandomSuggestion(suggestions) {
    const allSuggestions = suggestions.categories.flatMap(cat => cat.suggestions);
    if (allSuggestions.length > 0) {
        const randomIndex = Math.floor(Math.random() * allSuggestions.length);
        return allSuggestions[randomIndex];
    }
    return "No suggestions available.";
}

/**
 * Get suggestions by emotion (mood-based filtering).
 * @param {Object} suggestions - Dictionary containing suggestion categories
 * @param {string} emotion - The emotion to filter suggestions for
 * @returns {Array<string>} Filtered suggestions based on emotion
 */
function getSuggestionsByEmotion(suggestions, emotion) {
    const emotionMap = {
        'sadness': ['🤝 Social Connection', '💡 Creative Expression', '🧘‍♀️ Mindfulness & Relaxation'],
        'anger': ['💪 Stress Management', '🧘‍♀️ Mindfulness & Relaxation', '🏃‍♀️ Physical Wellness'],
        'fear': ['🧘‍♀️ Mindfulness & Relaxation', '🤝 Social Connection', '💪 Stress Management'],
        'joy': ['🎯 Personal Growth', '💡 Creative Expression', '🏃‍♀️ Physical Wellness'],
        'love': ['🤝 Social Connection', '💡 Creative Expression', '🎯 Personal Growth'],
        'surprise': ['💡 Creative Expression', '🎯 Personal Growth', '🏃‍♀️ Physical Wellness'],
        'disgust': ['🧘‍♀️ Mindfulness & Relaxation', '💪 Stress Management', '🌅 Morning Wellness'],
        'neutral': ['🎯 Personal Growth', '🏃‍♀️ Physical Wellness', '💡 Creative Expression']
    };
    
    const relevantCategories = emotionMap[emotion] || [];
    const relevantSuggestions = [];
    
    relevantCategories.forEach(categoryTitle => {
        const categorySuggestions = getSuggestionsByCategory(suggestions, categoryTitle);
        relevantSuggestions.push(...categorySuggestions);
    });
    
    return relevantSuggestions;
}

/**
 * Main function to demonstrate fetching and using suggestions.
 */
async function main() {
    console.log("🔍 Fetching wellness suggestions from the API...");
    
    try {
        // Fetch all suggestions
        const suggestions = await fetchAllSuggestions();
        
        if (!suggestions) {
            console.log("❌ Failed to fetch suggestions. Make sure the API is running.");
            return;
        }
        
        // Print all suggestions
        printSuggestions(suggestions);
        
        // Example: Get suggestions for a specific category
        console.log("\n" + "=".repeat(50));
        console.log("🎯 Example: Stress Management Suggestions");
        console.log("=".repeat(50));
        const stressSuggestions = getSuggestionsByCategory(suggestions, "💪 Stress Management");
        stressSuggestions.forEach((suggestion, index) => {
            console.log(`${index + 1}. ${suggestion}`);
        });
        
        // Example: Get a random suggestion
        console.log("\n" + "=".repeat(50));
        console.log("🎲 Random Suggestion of the Day");
        console.log("=".repeat(50));
        const randomSuggestion = getRandomSuggestion(suggestions);
        console.log(`💡 ${randomSuggestion}`);
        
        // Example: Get suggestions based on emotion
        console.log("\n" + "=".repeat(50));
        console.log("😊 Suggestions for Joy");
        console.log("=".repeat(50));
        const joySuggestions = getSuggestionsByEmotion(suggestions, 'joy');
        joySuggestions.slice(0, 5).forEach((suggestion, index) => {
            console.log(`${index + 1}. ${suggestion}`);
        });
        
        // Example: Save suggestions to a JSON file
        console.log("\n" + "=".repeat(50));
        console.log("💾 Saving suggestions to file...");
        try {
            fs.writeFileSync('wellness_suggestions.json', JSON.stringify(suggestions, null, 2));
            console.log("✅ Suggestions saved to 'wellness_suggestions.json'");
        } catch (error) {
            console.log(`❌ Error saving suggestions: ${error.message}`);
        }
        
    } catch (error) {
        console.error(`❌ Error: ${error.message}`);
    }
}

// Run the main function if this script is executed directly
if (require.main === module) {
    main();
}

// Export functions for use in other modules
module.exports = {
    fetchAllSuggestions,
    printSuggestions,
    getSuggestionsByCategory,
    getRandomSuggestion,
    getSuggestionsByEmotion
}; 