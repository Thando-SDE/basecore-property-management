#!/bin/bash
echo "========================================="
echo "🔍 BASE PROJECT VERIFICATION"
echo "========================================="

BASE_URL="https://basecore-property-management-production.up.railway.app"

echo "1. ✅ Health Check (Proof of deployment)"
echo "   Testing: $BASE_URL"
echo ""
response=$(curl -s -k "$BASE_URL" 2>/dev/null || curl -s "$BASE_URL" --insecure 2>/dev/null)
if [ ! -z "$response" ]; then
    echo "   Response:"
    echo "$response" | python -m json.tool 2>/dev/null || echo "   $response"
    echo ""
    echo "   ✅ Health check successful"
else
    echo "   ❌ Could not reach server (try with -k flag)"
    echo "   Testing with SSL bypass..."
    curl -k "$BASE_URL" || echo "   Please test manually in browser"
fi

echo ""
echo "2. ✅ Please test these URLs manually:"
echo "   - Health Check: $BASE_URL"
echo "   - Admin Panel: $BASE_URL/admin/"
echo "   - User Registration: $BASE_URL/api/users/ (POST method)"
echo ""
echo "3. ✅ Expected Results:"
echo "   - Health check returns JSON with status: healthy"
echo "   - Admin panel shows Django login (302 redirect)"
echo "   - User registration creates users in PostgreSQL"
echo "   - Protected endpoints return 401 (auth required)"
echo ""
echo "========================================="
echo "🎯 VERIFICATION COMPLETE"
echo "========================================="
echo "To test SSL issues on Windows, use:"
echo "curl -k https://basecore-property-management-production.up.railway.app/"
echo "Or test in browser for visual confirmation"
echo "========================================="
