#!/usr/bin/env python3
"""
Google OAuth Setup Script for Emotional Intelligence App
This script helps you set up Google OAuth authentication
"""

import os
import sys
from pathlib import Path

def print_banner():
    """Print setup banner"""
    print("=" * 60)
    print("🧠 Google OAuth Setup for Emotional Intelligence App")
    print("=" * 60)
    print()

def print_steps():
    """Print setup steps"""
    print("📋 Setup Steps:")
    print("1. Go to Google Cloud Console")
    print("2. Create a new project or select existing one")
    print("3. Enable Google+ API")
    print("4. Create OAuth 2.0 credentials")
    print("5. Configure authorized redirect URIs")
    print("6. Copy credentials to config.env")
    print()

def get_google_console_url():
    """Get Google Cloud Console URL"""
    return "https://console.cloud.google.com/"

def get_oauth_setup_url():
    """Get OAuth setup URL"""
    return "https://console.cloud.google.com/apis/credentials"

def print_detailed_steps():
    """Print detailed setup steps"""
    print("🔧 Detailed Setup Instructions:")
    print()
    
    print("1. 🌐 Go to Google Cloud Console:")
    print(f"   {get_google_console_url()}")
    print()
    
    print("2. 📁 Create/Select Project:")
    print("   - Click on project dropdown at the top")
    print("   - Click 'New Project' or select existing")
    print("   - Give it a name like 'Emotional Intelligence App'")
    print()
    
    print("3. 🔌 Enable APIs:")
    print("   - Go to 'APIs & Services' > 'Library'")
    print("   - Search for 'Google+ API'")
    print("   - Click 'Enable'")
    print()
    
    print("4. 🔑 Create OAuth Credentials:")
    print(f"   - Go to {get_oauth_setup_url()}")
    print("   - Click 'Create Credentials' > 'OAuth 2.0 Client IDs'")
    print("   - Choose 'Web application'")
    print("   - Name: 'Emotional Intelligence App'")
    print()
    
    print("5. 🔗 Configure Redirect URIs:")
    print("   - Add these authorized redirect URIs:")
    print("     * http://localhost:5001/auth/login/callback")
    print("     * http://127.0.0.1:5001/auth/login/callback")
    print("   - Click 'Create'")
    print()
    
    print("6. 📋 Copy Credentials:")
    print("   - Copy the Client ID and Client Secret")
    print("   - Add them to your config.env file")
    print()

def create_config_template():
    """Create config.env template"""
    config_path = Path("config.env")
    
    if config_path.exists():
        print("⚠️  config.env already exists!")
        response = input("Do you want to overwrite it? (y/N): ")
        if response.lower() != 'y':
            return
    
    config_content = """# Emotional Intelligence App Configuration

# Google OAuth Configuration
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here

# Flask Configuration
SECRET_KEY=your_secret_key_here
FLASK_ENV=development

# OpenAI Configuration (Optional - for AI insights)
OPENAI_API_KEY=your_openai_api_key_here

# Database Configuration
DATABASE_URL=sqlite:///data_and_models/instance/emotional_intelligence.db

# Server Configuration
PORT=5001
HOST=0.0.0.0
"""
    
    with open(config_path, 'w') as f:
        f.write(config_content)
    
    print("✅ Created config.env template")
    print("📝 Please edit config.env with your actual credentials")

def generate_secret_key():
    """Generate a secure secret key"""
    import secrets
    return secrets.token_hex(32)

def print_security_notes():
    """Print security notes"""
    print()
    print("🔒 Security Notes:")
    print("- Never commit config.env to version control")
    print("- Keep your Google Client Secret secure")
    print("- Use environment variables in production")
    print("- Regularly rotate your secret keys")
    print()

def main():
    """Main setup function"""
    print_banner()
    print_steps()
    
    while True:
        print("Choose an option:")
        print("1. Show detailed setup instructions")
        print("2. Create config.env template")
        print("3. Generate secret key")
        print("4. Show security notes")
        print("5. Exit")
        print()
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '1':
            print_detailed_steps()
        elif choice == '2':
            create_config_template()
        elif choice == '3':
            secret_key = generate_secret_key()
            print(f"🔑 Generated Secret Key: {secret_key}")
            print("Copy this to your config.env SECRET_KEY field")
        elif choice == '4':
            print_security_notes()
        elif choice == '5':
            print("👋 Setup complete! Good luck with your app!")
            break
        else:
            print("❌ Invalid choice. Please try again.")
        
        print()

if __name__ == "__main__":
    main() 