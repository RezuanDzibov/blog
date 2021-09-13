from django import template
from blog.models import Category, Article

register = template.Library()


@register.simple_tag
def get_categories():
    return Category.objects.all()


@register.simple_tag
def check_if_tags(article):
    try:
        tags = article.tags.all()
        tags[0]
        return True
    except IndexError:
        return False


