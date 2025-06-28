#!/usr/bin/env python3
"""
Google OAuth Setup Script for Emotional Intelligence App
This script helps you set up Google OAuth credentials for the application.
"""

import os
import webbrowser
from pathlib import Path

def print_banner():
    print("=" * 60)
    print("🔐 Google OAuth Setup for Mood Tracker")
    print("=" * 60)
    print()

def print_steps():
    print("📋 Follow these steps to set up Google OAuth:")
    print()
    print("1. 🌐 Go to Google Cloud Console")
    print("   https://console.cloud.google.com/")
    print()
    print("2. 📁 Create a new project or select existing one")
    print()
    print("3. 🔧 Enable the Google+ API:")
    print("   - Go to 'APIs & Services' > 'Library'")
    print("   - Search for 'Google+ API' and enable it")
    print()
    print("4. 🔑 Create OAuth 2.0 credentials:")
    print("   - Go to 'APIs & Services' > 'Credentials'")
    print("   - Click 'Create Credentials' > 'OAuth 2.0 Client IDs'")
    print("   - Choose 'Web application'")
    print()
    print("5. ⚙️ Configure OAuth consent screen:")
    print("   - App name: 'Mood Tracker'")
    print("   - User support email: your email")
    print("   - Developer contact information: your email")
    print()
    print("6. 🔗 Add authorized redirect URIs:")
    print("   - http://localhost:5001/auth/google/callback")
    print("   - https://yourdomain.com/auth/google/callback (for production)")
    print()
    print("7. 📋 Copy your credentials to config.env file")
    print()

def create_config_template():
    config_content = """# Flask Configuration
FLASK_SECRET_KEY=your-secret-key-here-change-this
FLASK_ENV=development

# Database Configuration
DATABASE_URL=sqlite:///emotional_intelligence.db

# Google OAuth Configuration
# Replace these with your actual Google OAuth credentials
GOOGLE_CLIENT_ID=your-google-client-id-here
GOOGLE_CLIENT_SECRET=your-google-client-secret-here
GOOGLE_DISCOVERY_URL=https://accounts.google.com/.well-known/openid_configuration

# Application Configuration
FRONTEND_URL=http://localhost:3000
API_URL=http://localhost:5001
"""
    
    config_path = Path("config.env")
    
    if config_path.exists():
        print("⚠️  config.env already exists!")
        response = input("Do you want to overwrite it? (y/N): ")
        if response.lower() != 'y':
            print("Setup cancelled.")
            return
    
    with open(config_path, 'w') as f:
        f.write(config_content)
    
    print("✅ Created config.env template")
    print("📝 Please edit config.env and add your Google OAuth credentials")

def open_google_console():
    print("🌐 Opening Google Cloud Console...")
    webbrowser.open("https://console.cloud.google.com/")
    print("✅ Google Cloud Console opened in your browser")

def main():
    print_banner()
    
    while True:
        print("Choose an option:")
        print("1. 📋 Show setup steps")
        print("2. 🌐 Open Google Cloud Console")
        print("3. 📝 Create config.env template")
        print("4. ✅ I'm done with setup")
        print("5. ❌ Exit")
        print()
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '1':
            print_steps()
        elif choice == '2':
            open_google_console()
        elif choice == '3':
            create_config_template()
        elif choice == '4':
            print()
            print("🎉 Setup complete!")
            print("Next steps:")
            print("1. Edit config.env with your Google OAuth credentials")
            print("2. Run: python3 api.py")
            print("3. Run: cd frontend && npm start")
            print("4. Visit http://localhost:3000")
            break
        elif choice == '5':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")
        
        print()

if __name__ == "__main__":
    main() 