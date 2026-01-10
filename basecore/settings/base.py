# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Ensure staticfiles directory exists
import os
if not os.path.exists(STATIC_ROOT):
    os.makedirs(STATIC_ROOT, exist_ok=True)

# WhiteNoise configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Add debug middleware in development
if DEBUG:
    MIDDLEWARE.append('basecore.middleware.DebugHeadersMiddleware')

# Force HTML middleware for admin
MIDDLEWARE.append('basecore.middleware.ForceHTMLContentTypeMiddleware')