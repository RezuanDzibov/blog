from django.urls.conf import include, path
from rest_framework import routers, urlpatterns
from . import views


router = routers.DefaultRouter()
router.register("user_profiles", views.UserProfileViewset)
router.register("social_links", views.SocialLinkViewSet)


urlpatterns = router.urls

