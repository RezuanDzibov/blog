from django.urls import path
from . import views

app_name = "article"

urlpatterns = [
    path("", views.ArticlesListView.as_view(), name="article_list"),
    path("article/<slug:slug>/", views.ArticleDetailView.as_view(), name="article_detail"),
    path("articles_by_author/<str:username>/", views.ArticlesByUser.as_view(), name="articles_by_user"),
    path("articles_by_you/", views.ArticlesByCurrentUser.as_view(), name="articles_by_current_user"),
    path("article_by_category/<slug:category_slug>/", views.ArticlesByCategoryListView.as_view(), name="articles_by_category"),
    path("article_by_tag/<slug:tag_slug>/", views.ArtcilesByTag.as_view(), name="articles_by_tag"),
    path("create_article/", views.ArticleCreateView.as_view(), name="create_article"),
    path("article_delete_confirm/<slug:slug>/", views.ArticleDelete.as_view(), name="delete_article_confirm"),
    path("article_edit/<slug:slug>/", views.ArticleUpdate.as_view(), name="article_edit"),
    path("add_comment/<str:article_slug>/", views.AddComment.as_view(), name="add_comment"),
    path("article_search/", views.ArticleSearch.as_view(), name="article_search"),
]
