import os, django, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault('DJANGO_SETTINGS_MODULE','mysite.settings')
django.setup()
from django.test import Client
from django.contrib.auth.models import User
from core.models import UserProfile

c = Client()
# create a sample user to delete
if not User.objects.filter(username='todelete').exists():
    u = User.objects.create_user(username='todelete', password='pwd', email='del@example.com')
    UserProfile.objects.update_or_create(user=u, defaults={'identificacion':'999','apodo':'todelete'})

print('before users:', User.objects.count(), 'profiles:', UserProfile.objects.count())
user = User.objects.get(username='todelete')
resp = c.post(f'/eliminar_usuario/{user.id}/', follow=True)
print('status', resp.status_code)
print('after users:', User.objects.count(), 'profiles:', UserProfile.objects.count())
print('exists?', User.objects.filter(username='todelete').exists())
