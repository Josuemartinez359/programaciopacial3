import os, django, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()
from core.models import UserProfile
for p in UserProfile.objects.select_related('user'):
    print('User:', p.user.username, 'identificacion:', p.identificacion, 'apodo:', p.apodo)
