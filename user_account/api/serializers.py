from rest_framework import serializers
from ..models import UserProfile
from blog.models import Article
from django.contrib.auth import get_user_model


User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'bio', 'social_links', 'avatar']


class UserSerializer(serializers.ModelSerializer):
    articles = serializers.PrimaryKeyRelatedField(many=True, queryset=Article.objects.filter(active=True))

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'user_profile', 'articles']