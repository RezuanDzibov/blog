from rest_framework import serializers
from ..models import Article


class ArticleSerializer(serializers.ModelSerializer):
    authors = serializers.ReadOnlyField(source='authors.username')
    
    class Meta:
        model = Article
        fields = ['id', 'title', 'authors', 'category', 'slug', 'text_body', 'created', 'published', 'image', 'active']

    