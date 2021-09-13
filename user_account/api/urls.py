from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('user_profiles/', views.UserProfileList.as_view()),
    path('user_profile/<int:pk>/', views.UserProfileDetail.as_view()),
    path('users/', views.UserList.as_view()),
    path('user/<int:pk>/', views.UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)