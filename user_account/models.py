from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from PIL import Image

User = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, related_name='user_profile')
    bio = models.TextField(max_length=5000, blank=True)
    avatar = models.ImageField(upload_to=f'avatars/%d/%m/%Y', blank=True)    

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse('user_account:my_profile', kwargs={'username': self.user.username})

    def save(self, *args, **kwargs):
        if self.avatar:
            super().save(*args, **kwargs)
            img = Image.open(self.avatar.path)
            if img.height > 300 or img.width > 275:
                output_size = (300, 275)
                img.thumbnail(output_size)
                img.save(self.avatar.path)


    
class SocialLink(models.Model):
    social_service_names = (
        ('pers_website', 'WebSite'),
        ('mail', 'Mail'),
        ('telegram', 'Telegram'),
        ('git', 'GitHub'),
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('insta', 'Instagram'),
        ('vk', 'VKontakte'),
        ('linkin', 'LindkedIn')
    )
    social_net_name = models.CharField(max_length=20, choices=social_service_names, default='')
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='social_links')
    url = models.URLField(max_length=200)

    def __str__(self) -> str:
        return f'{self.url}'
    

   