#!/usr/bin/env python3
"""
Test script to verify the authentication flow works correctly.
"""

import requests
import json

def test_authentication_flow():
    """Test the complete authentication flow"""
    base_url = "http://localhost:5001"
    
    print("🧪 Testing Authentication Flow")
    print("=" * 50)
    
    # Step 1: Check if user is authenticated (should not be)
    print("1. Checking initial authentication status...")
    response = requests.get(f"{base_url}/auth/user")
    print(f"   Status: {response.status_code}")
    if response.status_code == 401:
        print("   ✅ User not authenticated (expected)")
    else:
        print(f"   ❌ Unexpected status: {response.status_code}")
    
    # Step 2: Perform demo login
    print("\n2. Performing demo login...")
    session = requests.Session()
    response = session.get(f"{base_url}/auth/demo")
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Demo login successful")
        print(f"   User: {data['user']['name']} ({data['user']['email']})")
    else:
        print(f"   ❌ Demo login failed: {response.text}")
        return False
    
    # Step 3: Check if user is now authenticated
    print("\n3. Checking authentication after demo login...")
    response = session.get(f"{base_url}/auth/user")
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ User authenticated successfully")
        print(f"   User: {data['name']} ({data['email']})")
    else:
        print(f"   ❌ User not authenticated after demo login")
        return False
    
    # Step 4: Test protected endpoint
    print("\n4. Testing protected endpoint (analytics)...")
    response = session.get(f"{base_url}/analytics/summary")
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Analytics endpoint accessible")
        print(f"   Total entries: {data.get('total_entries', 0)}")
    else:
        print(f"   ❌ Analytics endpoint not accessible: {response.text}")
        return False
    
    # Step 5: Test AI insights endpoint
    print("\n5. Testing AI insights endpoint...")
    response = session.post(f"{base_url}/ai/insights", json={})
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ AI insights endpoint accessible")
        print(f"   Insights length: {len(data.get('insights', ''))}")
    else:
        print(f"   ❌ AI insights endpoint not accessible: {response.text}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All authentication tests passed!")
    return True

if __name__ == "__main__":
    try:
        success = test_authentication_flow()
        if success:
            print("\n✅ Authentication flow is working correctly!")
        else:
            print("\n❌ Authentication flow has issues!")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}") 