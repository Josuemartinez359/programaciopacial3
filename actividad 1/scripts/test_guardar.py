import os
import django
import sys
from pathlib import Path

# Ensure project root is on sys.path so 'mysite' module can be imported
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()
from django.test import Client
from django.contrib.auth.models import User
from core.models import UserProfile

c = Client()
resp = c.post('/guardar_usuario/', {
    'identificacion':'44444',
    'apodo':'apodoNew',
    'clave':'pwdZ',
    'nombre':'NombreZ',
    'apellido':'ApellidoZ',
    'email':'z@example.com'
}, follow=True)
print('status:', resp.status_code)
print('users:', User.objects.count())
print('profiles:', UserProfile.objects.count())
print('apodoNew user exists:', User.objects.filter(username='apodoNew').exists())
print('apodoNew email:', list(User.objects.filter(username='apodoNew').values_list('email', flat=True)))
print('apodoNew profile identificacion:', list(UserProfile.objects.filter(apodo='apodoNew').values_list('identificacion', flat=True)))
