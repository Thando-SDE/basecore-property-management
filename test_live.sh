#!/bin/bash
echo "=== LIVE APP TEST ==="
echo "Time: $(date)"
echo ""

# Test 1: Direct HTTP test
URL="https://basecore-property-management-production.up.railway.app"
echo "1. Testing $URL"
if curl -s -f -k --max-time 10 "$URL" > /dev/null 2>&1; then
    echo "   ✅ App is LIVE and responding"
    echo "   Response:"
    curl -s -k "$URL" | head -c 100
    echo "..."
else
    echo "   ❌ App is NOT responding (timeout or error)"
    echo "   Trying with verbose output:"
    curl -v -k --max-time 5 "$URL" 2>&1 | grep -i "HTTP\|connected\|failed"
fi

# Test 2: Check if we can get actual logs
echo -e "\n2. Checking Railway logs (last 2 minutes)..."
railway logs --since 2m --lines 5 2>/dev/null || echo "   Could not get recent logs"

# Test 3: Check Railway status
echo -e "\n3. Railway deployment status:"
railway status 2>/dev/null || echo "   Status command unavailable"

echo -e "\n=== Test complete ==="
