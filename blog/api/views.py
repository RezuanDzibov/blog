from rest_framework import generics
from .serializers import ArticleSerializer
from ..models import Article
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly

class ArticleList(generics.ListCreateAPIView):
    queryset = Article.objects.filter(active=True)
    serializer_class = ArticleSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(authors=self.request.user)

class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.filter(active=True)
    serializer_class = ArticleSerializer
    lookup_field = 'slug'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
