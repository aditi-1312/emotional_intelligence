#!/usr/bin/env python3
"""
Test script for authentication flow
"""

import requests
import json
import time

def test_auth_flow():
    """Test the complete authentication flow"""
    base_url = "http://localhost:5001"
    
    print("🔍 Testing Authentication Flow...")
    print("=" * 50)
    
    # Test 1: Health check
    print("1. Testing backend health...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Backend is running")
        else:
            print("❌ Backend health check failed")
            return False
    except Exception as e:
        print(f"❌ Backend connection failed: {e}")
        return False
    
    # Test 2: Google OAuth login endpoint
    print("\n2. Testing Google OAuth login endpoint...")
    try:
        response = requests.get(f"{base_url}/auth/login", allow_redirects=False)
        if response.status_code == 302:
            location = response.headers.get('Location', '')
            if 'accounts.google.com' in location:
                print("✅ Google OAuth login endpoint working (redirecting to Google)")
            else:
                print(f"❌ Unexpected redirect location: {location}")
                return False
        else:
            print(f"❌ Google OAuth login failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Google OAuth test failed: {e}")
        return False
    
    # Test 3: Demo login
    print("\n3. Testing demo login...")
    try:
        session = requests.Session()
        response = session.get(f"{base_url}/auth/demo")
        if response.status_code == 200:
            data = response.json()
            if 'user' in data and data['user']['name'] == 'Demo User':
                print("✅ Demo login working")
                demo_user = data['user']
            else:
                print("❌ Demo login returned unexpected data")
                return False
        else:
            print(f"❌ Demo login failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Demo login test failed: {e}")
        return False
    
    # Test 4: User authentication check
    print("\n4. Testing user authentication check...")
    try:
        response = session.get(f"{base_url}/auth/user")
        if response.status_code == 200:
            user_data = response.json()
            if user_data['name'] == 'Demo User':
                print("✅ User authentication check working")
                print(f"📄 User: {user_data['name']} ({user_data['email']})")
            else:
                print("❌ User authentication check returned unexpected data")
                return False
        else:
            print(f"❌ User authentication check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ User authentication check failed: {e}")
        return False
    
    # Test 5: Analytics endpoint (requires authentication)
    print("\n5. Testing authenticated endpoint...")
    try:
        response = session.get(f"{base_url}/analytics/summary")
        if response.status_code == 200:
            print("✅ Authenticated endpoint working")
        else:
            print(f"❌ Authenticated endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Authenticated endpoint test failed: {e}")
        return False
    
    # Test 6: Logout
    print("\n6. Testing logout...")
    try:
        response = session.get(f"{base_url}/auth/logout", allow_redirects=False)
        if response.status_code in [302, 200]:
            print("✅ Logout working")
        else:
            print(f"❌ Logout failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Logout test failed: {e}")
        return False
    
    # Test 7: Verify logout worked
    print("\n7. Verifying logout...")
    try:
        response = session.get(f"{base_url}/auth/user")
        if response.status_code == 401:
            print("✅ Logout verification successful (user not authenticated)")
        else:
            print(f"❌ Logout verification failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Logout verification failed: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All authentication tests passed!")
    print("\n📋 Summary:")
    print("- ✅ Backend is running")
    print("- ✅ Google OAuth login endpoint working")
    print("- ✅ Demo login working")
    print("- ✅ User authentication check working")
    print("- ✅ Authenticated endpoints working")
    print("- ✅ Logout working")
    print("\n🚀 Authentication system is fully functional!")
    
    return True

if __name__ == "__main__":
    test_auth_flow()
