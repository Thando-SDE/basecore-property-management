import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'basecore.settings')
import django
django.setup()

print("Django setup complete")
print("Trying to import payments.views...")

try:
    from payments import views
    print("SUCCESS: payments.views imported")
except ImportError as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
