from django.urls import path
from . import views

app_name = 'user_account'


urlpatterns = [
    path('profiles/', views.UserProfileListView.as_view(), name='profiles'),
    # path('my_profile/', views.MyProfile.as_view(), name='my_profile'),
    path('profile/<str:username>/' , views.UserProfileView.as_view(), name='profile'),
    path('profile/<str:username>/update/', views.UserDataUpdateView.as_view(), name='update_profile'),
    path('user_search/', views.UserProfileSearch.as_view(), name='search_user'),
    path('add_social_network_link/<str:soc_net_name>/', views.AddSocialNetworkLink.as_view(), name='add_soc_net_link')
]
