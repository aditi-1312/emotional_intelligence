#!/usr/bin/env python3
"""
🚀 Emotional Intelligence API Runner
====================================

Simple script to run the Flask API with proper configuration.
"""

import os
import sys
from api import app

if __name__ == "__main__":
    # Set environment variables
    os.environ.setdefault('FLASK_DEBUG', 'True')
    os.environ.setdefault('PORT', '5001')
    os.environ.setdefault('HOST', '0.0.0.0')
    
    print("🧠 Emotional Intelligence API")
    print("=" * 40)
    print(f"🚀 Starting Flask API server...")
    print(f"📱 API will be available at: http://localhost:{os.environ.get('PORT', 5001)}")
    print(f"⏹️  Press Ctrl+C to stop the server")
    
    try:
        app.run(
            host=os.environ.get('HOST', '0.0.0.0'),
            port=int(os.environ.get('PORT', 5001)),
            debug=os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
        )
    except KeyboardInterrupt:
        print("\n👋 API server stopped.")
    except Exception as e:
        print(f"❌ Error starting API server: {e}")
        sys.exit(1) 