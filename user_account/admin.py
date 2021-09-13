from django.contrib import admin
from . import models

@admin.register(models.UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user"]
    list_diplay_links = ["user"]

@admin.register(models.SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ["user_profile", "url"]
    list_display_links = ["user_profile"]
