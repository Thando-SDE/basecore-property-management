import requests
import json

BASE_URL = "https://basecore-property-management-production.up.railway.app"

print("Testing JWT Authentication...")

# Test registration
data = {
    "username": "test_jwt_" + str(hash(BASE_URL))[-4:],
    "email": f"test{hash(BASE_URL)[-4:]}@example.com",
    "password": "TestJwt123!",
    "password2": "TestJwt123!"
}

print(f"1. Registering user: {data['username']}")
response = requests.post(f"{BASE_URL}/api/users/", json=data, verify=False)
print(f"   Status: {response.status_code}")
print(f"   Response: {json.dumps(response.json(), indent=2) if response.status_code == 201 else response.text}")

if response.status_code == 201:
    resp_data = response.json()
    if 'access' in resp_data:
        print("\n✅ JWT TOKENS ARE WORKING!")
        print(f"   Access token received: {resp_data['access'][:50]}...")
        
        # Test protected endpoint
        headers = {"Authorization": f"Bearer {resp_data['access']}"}
        print("\n2. Testing protected endpoint with token...")
        response = requests.get(f"{BASE_URL}/api/properties/", headers=headers, verify=False)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:100]}...")
    else:
        print("\n⚠️  JWT tokens not in response (old code still running)")
else:
    print("\n❌ Registration failed")
