import os
import sys

# Read production settings
with open('basecore/settings/production.py', 'r') as f:
    content = f.read()

# Add SimpleJWT to INSTALLED_APPS if not there
if "'rest_framework_simplejwt'" not in content:
    # Find INSTALLED_APPS and add it
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        new_lines.append(line)
        if "INSTALLED_APPS" in line and "'rest_framework_simplejwt'" not in content:
            # Find where to insert (after rest_framework)
            pass
    # Simplified: just append
    if "'rest_framework_simplejwt'" not in content:
        content = content.replace(
            "'rest_framework',",
            "'rest_framework',\n    'rest_framework_simplejwt',"
        )

# Add REST_FRAMEWORK settings if not there
if "REST_FRAMEWORK" not in content:
    jwt_config = '''
# JWT Authentication
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
}
'''
    # Add after database config
    if "DATABASES" in content:
        parts = content.split("DATABASES")
        content = parts[0] + "DATABASES" + parts[1].split('\n\n', 1)[0] + '\n\n' + jwt_config + parts[1].split('\n\n', 1)[1]

with open('basecore/settings/production.py', 'w') as f:
    f.write(content)

print("✅ Updated production.py with JWT settings")
