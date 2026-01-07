@echo off
echo ========================================
echo BASE PROJECT TEST - WINDOWS
echo ========================================
echo.
echo This script helps test the BaseCore API on Windows.
echo Windows sometimes has SSL certificate issues with Railway.
echo.
echo Option 1: Test in browser (RECOMMENDED)
echo   1. Open: https://basecore-property-management-production.up.railway.app/
echo   2. Should see: {"status": "healthy", "service": "BaseCore"}
echo.
echo Option 2: Use curl with -k flag
echo   curl -k https://basecore-property-management-production.up.railway.app/
echo.
echo Option 3: Use Python (if installed)
echo   python test_with_python.py
echo.
echo ========================================
echo TEST URLs:
echo ========================================
echo Health Check: https://basecore-property-management-production.up.railway.app/
echo Admin Panel:  https://basecore-property-management-production.up.railway.app/admin/
echo API Docs:     See README.md for endpoint documentation
echo ========================================
pause
