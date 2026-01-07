#!/bin/bash
echo "========================================="
echo "🚀 JWT TESTING VIA CLI (Railway health check ignored)"
echo "========================================="

BASE_URL="https://basecore-property-management-production.up.railway.app"

echo "1. ✅ Health check (direct curl):"
curl -k --max-time 10 "$BASE_URL" 2>/dev/null || echo "   ⚠️  Direct curl failed, checking alternative..."

# Alternative: Test through a proxy-like approach
echo -e "\n2. 🔧 Testing if app is actually reachable:"
timeout 5 curl -s -I "$BASE_URL" 2>/dev/null | head -1 && echo "   ✅ App is reachable!" || echo "   ❌ App not reachable"

echo -e "\n3. 👤 Testing user registration with JWT return:"
curl -k -X POST "$BASE_URL/api/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "jwt_test_'$(date +%s)'",
    "email": "jwt_test@example.com",
    "password": "JwtTest123!",
    "password2": "JwtTest123!"
  }' 2>/dev/null | head -c 150

echo -e "\n\n4. 🔑 Testing JWT token endpoint:"
curl -k -X POST "$BASE_URL/api/token/" \
  -H "Content-Type: application/json" \
  -d '{"username": "simple_test", "password": "SimpleTest123!"}' 2>/dev/null | head -c 100

echo -e "\n\n5. 🛡️ Testing protected endpoint (should fail without token):"
curl -k -I "$BASE_URL/api/properties/" 2>/dev/null | head -1

echo -e "\n========================================="
echo "📊 ASSESSMENT:"
echo "If step 3 returns tokens → JWT WORKS"
echo "If step 4 returns access token → JWT WORKS"
echo "If step 5 returns 401 → PROTECTION WORKS"
echo "========================================="
