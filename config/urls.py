from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from user_account import views as user_account_views
from .yasg import urlpatterns as doc_urls
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/signin/", user_account_views.LoginView.as_view(), name="signin"),
    path("accounts/signup/", user_account_views.RegisterCreateView.as_view(), name="signup"),
    path("accounts/signout/", LogoutView.as_view(), name="some"),
    path("accounts/",  include("django.contrib.auth.urls")),
    path("accounts/", include("user_account.urls", namespace="user_profile")),
    path("api-auth/", include("djoser.urls")),
    path("api-auth/", include("djoser.urls.authtoken")),
    path("api-auth/", include("djoser.urls.jwt")),
    path("api/v1/user_account/", include("user_account.api.urls")),
    path("api/v1/blog/", include("blog.api.urls")),
    path("", include("blog.urls", namespace="blog")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
]


urlpatterns += doc_urls


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)