import django
from user_account.models import SocialLink
from django import template

register = template.Library()


@register.simple_tag
def get_link(user_profile, soc_net_name):
    try:
        link = user_profile.social_links.get(social_net_name=soc_net_name)
        return link
    except SocialLink.DoesNotExist:
        return False

