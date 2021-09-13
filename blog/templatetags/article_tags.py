from django import template
from blog import models

register = template.Library()


@register.simple_tag
def get_categories():
    return models.Category.objects.all()


@register.simple_tag
def check_if_tags(article):
    tags = article.tags.all()
    if tags.exists():
        return True
    return False


