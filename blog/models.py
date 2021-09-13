from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from user_account.models import UserProfile
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField


User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:

        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def save(self):
        self.slug = slugify(self.name)
        super().save()
    

class Article(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=100, unique_for_date='created', blank=True)
    text_body = RichTextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    published = models.DateTimeField(default=timezone.now)
    authors = models.ForeignKey(User, related_name='articles', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='articles', on_delete=models.PROTECT, default='')
    image = models.ImageField(upload_to='%d/%m/%Y', blank=True)
    active = models.BooleanField(default=True)

    tags = TaggableManager(blank=True)

    class Meta:
        verbose_name = 'article'
        verbose_name_plural = 'articles'
        ordering = ['-created']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:article_detail', args=[self.created.day, self.created.month, self.created.year, self.slug])

    def save(self):
        self.slug = slugify(self.title)
        super(Article, self).save()

    def get_last_five_comments(self):
        return self.comments.filter(status=True).order_by('-created')[:5]



class Comment(models.Model):
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(UserProfile, related_name='comments', on_delete=models.CASCADE)
    text_body = models.TextField(max_length=5000)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)


    def __str__(self):
        return self.text_body[:20]

