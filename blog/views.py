from django.shortcuts import render, get_object_or_404, redirect
from django.utils.datastructures import MultiValueDictKeyError
from . import models
from django.contrib.auth import get_user_model
from . import forms
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from taggit.models import Tag
from django.views import generic
from base import mixins as project_mixins
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.postgres.search import SearchVector


User = get_user_model()


class ArticlesListView(project_mixins.ArticleListMixin):
    queryset = models.Article.objects.filter(active=True)


class ArticlesByCategoryListView(project_mixins.ArticleListMixin):
    def get_queryset(self):
        self.category = get_object_or_404(models.Category, slug=self.kwargs["category_slug"])
        self.articles = models.Article.objects.filter(active=True, category=self.category)
        return self.articles

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_category"] = self.category
        return context


class ArticlesByUser(project_mixins.ArticleListMixin):
    def get_queryset(self):
        self.author = get_object_or_404(User, username=self.kwargs["username"])
        self.articles = models.Article.objects.filter(active=True, authors=self.author)
        return self.articles

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["author"] = self.author
        return context


class ArticlesByCurrentUser(generic.base.View):
    def get(self, request):
        articles = models.Article.objects.filter(active=True, author=request.user)
        return render(request, "article/article_list.html", {"current_author": request.user, "articles": articles})


class ArtcilesByTag(generic.base.View):
    def get(self, request, tag_slug):
        tag = get_object_or_404(Tag, slug=tag_slug)
        articles = models.Article.objects.filter(active=True, tags__in=[tag])
        return render(request, "article/article_list.html", {"tag": tag, "articles": articles})


class ArticleDetailView(generic.detail.DetailView, project_mixins.AddToContextMixin):
    model = models.Article
    template_name = "article/article_detail.html"
    context_dict = {"comment_form": forms.CommentForm()}


class AddComment(generic.base.View, SuccessMessageMixin):
    def post(self, request, article_slug):
        form = forms.CommentForm(request.POST)
        article = models.Article.objects.get(slug=article_slug)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.article = article
            form.save()
        messages.success(request, "Comment added successfully")
        return redirect(article.get_absolute_url())


class ArticleCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.edit.CreateView):
    model = models.Article
    template_name = "article/article_create.html"
    form_class = forms.ArticleForm
    success_message = "Article created successfully"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleUpdate(project_mixins.IsOwnerOrRedirect, generic.edit.UpdateView):
    model = models.Article
    form_class = forms.ArticleForm
    template_name = "article/article_update.html"
    owner_field_name = "author"


class ArticleDelete(project_mixins.IsOwnerOrRedirect, generic.edit.DeleteView):
    model = models.Article
    template_name = "article/article_confirm_delete.html"
    context_object_name = "article"
    success_url = reverse_lazy("blog:article_list")
    owner_field_name = "author"


class ArticleSearch(project_mixins.ArticleListMixin):
    def get_queryset(self):
        try:
            queryset = models.Article.objects.annotate(search=SearchVector("title", "text_body")).filter(search=self.request.GET["q"], active=True)
        except MultiValueDictKeyError: 
            queryset = super().get_queryset()  
        return queryset

    def get_context_data(self, *args, **kwargs):
        context =  super().get_context_data(*args, **kwargs)
        try:
            context["q"] = self.request.GET["q"]
        except MultiValueDictKeyError:
            pass
        return context
