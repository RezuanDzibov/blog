from django.contrib import admin
from .models import UserProfile, SocialLink

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user']
    list_diplay_links = ['user']

@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ['user_profile', 'url']
    list_display_links = ['user_profile']

