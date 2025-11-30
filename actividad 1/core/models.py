from django.db import models
from django.conf import settings


class UserProfile(models.Model):
	"""Perfil simple asociado a un User para almacenar identificación y apodo."""
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
	identificacion = models.CharField(max_length=64, blank=True, null=True)
	apodo = models.CharField(max_length=150, blank=True, null=True)

	def __str__(self) -> str:
		return f"Profile: {self.user.username}"
