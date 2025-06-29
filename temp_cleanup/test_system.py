#!/usr/bin/env python3
"""
Comprehensive test script for the Emotional Intelligence application
"""

import requests
import json
import time
import sys

BASE_URL = "http://localhost:5001"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_text_analysis():
    """Test text analysis endpoint"""
    print("\n🔍 Testing text analysis...")
    try:
        test_texts = [
            "I am feeling happy and excited today!",
            "I'm really sad and disappointed about what happened.",
            "I'm angry about the way I was treated.",
            "I'm scared about the upcoming presentation."
        ]
        
        for text in test_texts:
            response = requests.post(
                f"{BASE_URL}/analyze",
                json={"text": text},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                emotion = data.get('analysis', {}).get('dominant_emotion', 'unknown')
                confidence = data.get('analysis', {}).get('confidence', 0)
                print(f"✅ '{text[:30]}...' → {emotion} ({confidence:.2f})")
            else:
                print(f"❌ Analysis failed for '{text[:30]}...': {response.status_code}")
                return False
        return True
    except Exception as e:
        print(f"❌ Text analysis error: {e}")
        return False

def test_demo_login():
    """Test demo login"""
    print("\n🔍 Testing demo login...")
    try:
        response = requests.get(f"{BASE_URL}/auth/demo")
        if response.status_code == 200:
            data = response.json()
            user = data.get('user', {})
            print(f"✅ Demo login successful: {user.get('name', 'Unknown')}")
            return True
        else:
            print(f"❌ Demo login failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Demo login error: {e}")
        return False

def test_journal_entries():
    """Test journal entry creation and retrieval"""
    print("\n🔍 Testing journal entries...")
    try:
        # Create a session to maintain cookies
        session = requests.Session()
        
        # First, do demo login to get authenticated
        login_response = session.get(f"{BASE_URL}/auth/demo")
        if login_response.status_code != 200:
            print(f"❌ Demo login failed for journal test: {login_response.status_code}")
            return False
        
        # Test adding a journal entry
        test_entry = "I'm feeling optimistic about my new project and excited to see where it leads."
        response = session.post(
            f"{BASE_URL}/journal",
            json={"text": test_entry, "user_id": "user123"},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            print("✅ Journal entry created successfully")
            
            # Test retrieving journal entries
            response = session.get(f"{BASE_URL}/journal?user_id=user123&limit=5")
            if response.status_code == 200:
                entries = response.json()
                print(f"✅ Retrieved {len(entries)} journal entries")
                return True
            else:
                print(f"❌ Failed to retrieve journal entries: {response.status_code}")
                return False
        else:
            print(f"❌ Failed to create journal entry: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Journal entries error: {e}")
        return False

def test_analytics():
    """Test analytics endpoints"""
    print("\n🔍 Testing analytics...")
    try:
        # Create a session to maintain cookies
        session = requests.Session()
        
        # First, do demo login to get authenticated
        login_response = session.get(f"{BASE_URL}/auth/demo")
        if login_response.status_code != 200:
            print(f"❌ Demo login failed for analytics test: {login_response.status_code}")
            return False
        
        # Test analytics summary
        response = session.get(f"{BASE_URL}/analytics/summary?user_id=user123")
        if response.status_code == 200:
            data = response.json()
            total_entries = data.get('total_entries', 0)
            print(f"✅ Analytics summary: {total_entries} total entries")
            
            # Test timeline
            response = session.get(f"{BASE_URL}/analytics/timeline?user_id=user123")
            if response.status_code == 200:
                timeline = response.json()
                print(f"✅ Timeline: {len(timeline)} entries")
                return True
            else:
                print(f"❌ Timeline failed: {response.status_code}")
                return False
        else:
            print(f"❌ Analytics summary failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Analytics error: {e}")
        return False

def test_ai_insights():
    """Test AI insights endpoint"""
    print("\n🔍 Testing AI insights...")
    try:
        # Create a session to maintain cookies
        session = requests.Session()
        
        # First, do demo login to get authenticated
        login_response = session.get(f"{BASE_URL}/auth/demo")
        if login_response.status_code != 200:
            print(f"❌ Demo login failed for AI insights test: {login_response.status_code}")
            return False
        
        response = session.post(
            f"{BASE_URL}/ai/insights",
            json={"user_id": "user123"},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            insights = response.text
            print(f"✅ AI insights generated ({len(insights)} characters)")
            return True
        else:
            print(f"❌ AI insights failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ AI insights error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧠 Emotional Intelligence System Test")
    print("=" * 50)
    
    tests = [
        test_health,
        test_text_analysis,
        test_demo_login,
        test_journal_entries,
        test_analytics,
        test_ai_insights
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        time.sleep(1)  # Brief pause between tests
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The system is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the system configuration.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 