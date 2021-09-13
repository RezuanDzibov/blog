from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import UserProfile


# def profile(sender, instance, created, **kwargs):
# 	if created:
# 		UserProfile.objects.create(user=instance)

# post_save.connect(profile, sender=User)