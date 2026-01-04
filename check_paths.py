import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'basecore.settings')
import django
django.setup()

import sys
print("Python paths during Django runtime:")
for p in sys.path:
    print(f"  {p}")

print("\nTrying to find stripe...")
try:
    import stripe
    print(f"Stripe found at: {stripe.__file__}")
except ImportError:
    print("Stripe NOT found in Django runtime!")
