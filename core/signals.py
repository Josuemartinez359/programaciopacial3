from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import UserProfile


@receiver(post_save, sender=get_user_model())
def ensure_user_profile(sender, instance, created, **kwargs):
    """Create a UserProfile if a User was created, or ensure it exists.

    This keeps the DB consistent even if users are created somewhere else
    (e.g. admin, fixtures) and prevents missing profile lookups.
    """
    if created:
        UserProfile.objects.create(user=instance)
    else:
        UserProfile.objects.get_or_create(user=instance)
