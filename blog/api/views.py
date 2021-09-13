from rest_framework import viewsets, generics
from .. import models
from rest_framework import permissions
from .permissions import IsAuthorOrReadOnly
from . import serializers
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter
from . import services
from rest_framework import pagination
from base import api_mixins


class ArticleViewSet(api_mixins.SerializerByAction, viewsets.ModelViewSet):
    queryset = models.Article.objects.filter(active=True)
    default_serializer_class = serializers.ArticleDetailSerializer
    serializer_classes = {
        "list": serializers.ArticleListSerializer, 
        "create": serializers.ArticleUpdateCreateSerializer,
        "update": serializers.ArticleUpdateCreateSerializer,
        "partial_update": serializers.ArticleUpdateCreateSerializer 
    }
    lookup_field = "slug"
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    filter_backends = (filters.DjangoFilterBackend, SearchFilter)
    filterset_fields = ("category", "author", "tags__name")
    author_field_name = "author"
    search_fields = ("title", "text_body", "tags__name")
    pagination_class = pagination.PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ArticlesByYou(generics.ListAPIView):
    serializer_class = serializers.ArticleListSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = pagination.PageNumberPagination

    def get_queryset(self):
        user = self.request.user
        return models.Article.objects.filter(active=True, author=user)
        

class CommentViewSet(viewsets.ModelViewSet):
    queryset = models.Comment.objects.filter(status=True)
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    author_field_name = "author"
    pagination_class = services.CommentPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)