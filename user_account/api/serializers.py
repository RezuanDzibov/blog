from rest_framework import serializers
from .. import models
from django.contrib.auth import get_user_model


User = get_user_model()


class UrlHyperlinkedIdentityField(serializers.HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        if obj.pk is None:
            return None
        return self.reverse(view_name, kwargs={"username": obj.user.username}, request=request, format=format)


class SocialLinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SocialLink
        fields = ("id", "user_profile", "social_net_name", "url")
        read_only_fields = ("user_profile",)


class SocailLinksSerizalizerByUserProfile(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    social_links = SocialLinkSerializer(many=True)

    class Meta:
        model = models.UserProfile
        fields = ("username", "social_links")


class UserProfileListSerizalizer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.CharField(source="user.email")
    url = UrlHyperlinkedIdentityField("userprofile-detail")

    class Meta:
        model = models.UserProfile
        fields = ("username", "first_name", "last_name", "email", "bio", "url")

  
class UserProfileDetailSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.CharField(source="user.email")
    social_links = SocialLinkSerializer(many=True)

    class Meta:
        model = models.UserProfile
        fields = ("username", "first_name", "last_name", "email", "bio", "avatar", "social_links")


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    social_links = SocialLinkSerializer(many=True)
    
    class Meta:
        model = models.UserProfile
        fields = ("first_name", "last_name", "bio", "avatar", "social_links")
    




