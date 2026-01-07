import requests
import json
import sys

BASE_URL = "https://basecore-property-management-production.up.railway.app"

def test_health_check():
    """Test if the API is responding"""
    print("1. Testing health check...")
    try:
        response = requests.get(BASE_URL, verify=False, timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ API is LIVE: {data}")
            return True
        else:
            print(f"   ❌ Unexpected status: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Connection error: {e}")
        print("   Tip: Windows may block SSL. Try in browser instead.")
        return False

def test_user_registration():
    """Test user registration endpoint"""
    print("\n2. Testing user registration...")
    import time
    username = f"test_user_{int(time.time())}"
    user_data = {
        "username": username,
        "email": f"{username}@test.com",
        "password": "TestPass123!",
        "password2": "TestPass123!"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/users/",
            json=user_data,
            verify=False,
            timeout=10
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            print(f"   ✅ User '{username}' created successfully")
            return True
        else:
            print(f"   ❌ Registration failed: {response.text[:100]}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_protected_endpoint():
    """Test that protected endpoints require auth"""
    print("\n3. Testing authentication system...")
    try:
        response = requests.get(
            f"{BASE_URL}/api/properties/",
            verify=False,
            timeout=10
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 401:
            print("   ✅ CORRECT: 401 means authentication required")
            return True
        else:
            print(f"   ⚠️  Got {response.status_code} (expected 401)")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    print("=" * 50)
    print("BaseCore API Test - Python")
    print("=" * 50)
    print(f"Testing URL: {BASE_URL}")
    print("")
    
    tests = [
        test_health_check,
        test_user_registration,
        test_protected_endpoint
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    if all(results):
        print("🎉 ALL TESTS PASSED!")
        print("✅ API is live and functional")
        print("✅ User registration works")
        print("✅ Authentication system active")
    else:
        print("⚠️  Some tests failed")
        print("Tip: Windows SSL issues are common with Railway")
        print("     Test manually in browser:")
        print(f"     - {BASE_URL}")
        print(f"     - {BASE_URL}/admin/")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
