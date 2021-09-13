from .. import models
from . import serializers
from rest_framework import generics, mixins, viewsets, permissions
from django.contrib.auth import get_user_model
from .permissions import IsAuthorOrReadOnly
from rest_framework.filters import SearchFilter
from rest_framework import validators, views
from . import services
from rest_framework.response import Response
from base import api_mixins


User = get_user_model()


class UserProfileViewset(
    api_mixins.SerializerByAction, 
    mixins.ListModelMixin, 
    mixins.UpdateModelMixin, 
    mixins.RetrieveModelMixin, 
    mixins.DestroyModelMixin, 
    viewsets.GenericViewSet, 
):
    queryset = models.UserProfile.objects.filter(user__is_active=True)
    default_serializer_class = serializers.UserProfileDetailSerializer
    serializer_classes = {
        "list": serializers.UserProfileListSerizalizer, 
        "update": serializers.UserProfileUpdateSerializer, 
        "partial_update": serializers.UserProfileUpdateSerializer
    }
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    filter_backends = (SearchFilter,)
    search_fields = ("user__username", "user__email", "user__first_name", "user__last_name")
    author_field_name = "user"
    lookup_field = "user__username"
    lookup_url_kwarg = "username"
    pagination_class = services.UserProfilePagination


class SocialLinkViewSet(viewsets.ModelViewSet):
    queryset = models.SocialLink.objects.filter(user_profile__user__is_active=True)
    serializer_class = serializers.SocialLinkSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    author_field_name = "user_profile"
    pagination_class = services.SocialLinkPagination
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(models.UserProfile.objects.filter(user__is_active=True))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializers.SocailLinksSerizalizerByUserProfile(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = serializers.SocailLinksSerizalizerByUserProfile(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        link = self.request.user.user_profile.social_links.filter(social_net_name=serializer.validated_data["social_net_name"])
        if link.exists():
            raise validators.ValidationError("The link to the social network profile already exists")  
        serializer.save(user_profile=self.request.user.user_profile)    
            