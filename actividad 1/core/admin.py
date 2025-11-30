from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'identificacion', 'apodo')
	search_fields = ('user__username', 'identificacion', 'apodo')
