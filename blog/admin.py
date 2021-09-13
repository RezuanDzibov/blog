from django.contrib import admin
from .models import Category, Article, Comment
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class BlogAdminForm(forms.ModelForm):
    text_body = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Article
        fields = "__all__"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):    
    list_display = ("name",)
    list_display_links = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "author", "slug", "created", "published", "active")
    list_display_links = ("title", "category", "author")
    list_editable = ("active",)
    prepopulated_fields = {"slug": ("title",)}
    form = BlogAdminForm


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("article", "author", "created", "status")
    list_display_links = ("article", "author")
    list_editable = ("status",)