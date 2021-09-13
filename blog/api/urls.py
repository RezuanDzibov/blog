from . import views
from django.urls import path
from rest_framework import routers

router = routers.DefaultRouter()
router.register("articles", views.ArticleViewSet)
router.register("comments", views.CommentViewSet)


urlpatterns = [
    path("articles_by_you/", views.ArticlesByYou.as_view()),
    
]


urlpatterns += router.urls