import os
import sys
import django
from pathlib import Path

# Ensure project root is on sys.path so 'mysite' settings can be imported
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()
from django.contrib.auth import get_user_model
from core.models import UserProfile

User = get_user_model()
count = 0
for u in User.objects.all():
    try:
        _ = u.profile
    except Exception:
        UserProfile.objects.create(user=u)
        count += 1

print('created profiles for %d users' % count)
