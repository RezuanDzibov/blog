from rest_framework import pagination


class UserProfilePagination(pagination.PageNumberPagination):
    page_size = 6


class SocialLinkPagination(pagination.PageNumberPagination):
    page_size = 6