from rest_framework import serializers
from .. import models
from taggit.serializers import TaggitSerializer, TagListSerializerField


class ArticleListSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    url = serializers.HyperlinkedIdentityField("article-detail", lookup_field="slug")
    
    class Meta:
        model = models.Article
        fields = ("title", "slug", "author", "category", "active", "url")


class ArticleDetailSerializer(TaggitSerializer, serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    tags = TagListSerializerField()
    comments = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = models.Article
        fields = ("title", "slug", "author", "category", "text_body", "created", "published", "image", "active", "tags", "comments")


class ArticleUpdateCreateSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField(required=False)

    class Meta:
        model = models.Article
        fields = ("title", "category", "text_body", "published", "image", "active", "tags")


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = models.Comment
        fields = ("article", "text_body", "author")
