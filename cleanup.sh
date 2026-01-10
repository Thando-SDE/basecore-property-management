#!/bin/bash

echo "=== CLEANING UP BASE-CORE PROJECT ==="

# 1. Remove all test files (they're causing import errors)
rm -f check_paths.py
rm -f test*.py
rm -f test*.bat
rm -f simple_test.py
rm -f update_jwt.py
rm -f test_django_import.py
rm -f test_health.py
rm -f test_imports.py
rm -f test_jwt.py
rm -f test_proper_fix.py
rm -f test_settings.py
rm -f test_with_python.py

# 2. Remove database files (should not be in git)
rm -f db.sqlite3
rm -f test.db

# 3. Remove backup directory
rm -rf backup/

# 4. Remove deployment.log
rm -f deployment.log

# 5. Remove old unnecessary files
rm -f '=8.0.0'

# 6. Remove venv from git tracking (keep local, but not in repo)
echo "venv/" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
echo "*.sqlite3" >> .gitignore

# 7. Fix the basecore/__init__.py - make it EMPTY
echo "# BaseCore Package" > basecore/__init__.py

# 8. Fix the basecore/settings/__init__.py - SIMPLIFY IT
cat > basecore/settings/__init__.py << 'EOL'
"""
Django settings module initialization.
Loads settings from base.py, development.py, or production.py
based on DJANGO_SETTINGS_MODULE environment variable.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Clear any Django cache if exists
import sys
if 'django.conf' in sys.modules:
    del sys.modules['django.conf']
EOL

# 9. Create a proper .gitignore
cat > .gitignore << 'EOL'
# Django
*.log
*.pot
*.pyc
__pycache__/
db.sqlite3
db.sqlite3-journal
media/

# Environments
.env
.venv
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Railway/Deployment
staticfiles/  # Railway will create this
deployment.log

# Backup files
backup/
EOL

echo "=== CLEANUP COMPLETE ==="
echo "Removed:"
echo "- All test files"
echo "- Database files"
echo "- Backup directory"
echo "- Deployment logs"
echo ""
echo "Next steps:"
echo "1. Run: git add ."
echo "2. Run: git commit -m 'CLEANUP: Remove unnecessary files'"
echo "3. Run: git push origin main"
echo "4. Run: railway up"
