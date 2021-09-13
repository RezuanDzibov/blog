from django.shortcuts import render, get_object_or_404, redirect
from django.utils.datastructures import MultiValueDictKeyError
from .models import Category, Article
from django.contrib.auth.models import User
from .forms import ArticleForm,  CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from taggit.models import Tag
from django.views import generic
from utilets.mixins import ArticleListMixin, AddToContextMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.postgres.search import SearchVector


class ArticlesListView(ArticleListMixin):
    queryset = Article.objects.filter(active=True)


class ArticlesByCategoryListView(ArticleListMixin):
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        self.articles = Article.objects.filter(active=True, category=self.category)
        return self.articles

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_category'] = self.category
        return context


class ArticlesByUser(ArticleListMixin):
    def get_queryset(self):
        self.author = get_object_or_404(User, username=self.kwargs['username'])
        self.articles = Article.objects.filter(active=True, authors=self.author)
        return self.articles

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.author
        return context


class ArticlesByCurrentUser(generic.base.View):
    def get(self, request):
        author = get_object_or_404(User, username=request.user.username)
        articles = Article.objects.filter(active=True, authors=author)
        return render(request, 'article/article_list.html', {'current_author': author, 'articles': articles})


class ArtcilesByTag(generic.base.View):
    def get(self, request, tag_slug):
        tag = get_object_or_404(Tag, slug=tag_slug)
        articles = Article.objects.filter(active=True, tags__in=[tag])
        return render(request, 'article/article_list.html', {'tag': tag, 'articles': articles})


class ArticleDetailView(generic.detail.DetailView, AddToContextMixin):
    model = Article
    template_name = 'article/article_detail.html'
    context_dict = {'comment_form': CommentForm()}


class AddComment(generic.base.View, SuccessMessageMixin):
    def post(self, request, article_slug):
        form = CommentForm(request.POST)
        article = Article.objects.get(slug=article_slug)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user.user_profile
            form.article = article
            form.save()
        messages.success(request, 'Comment added successfully')
        return redirect(article.get_absolute_url())


class ArticleCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.edit.CreateView):
    model = Article
    template_name = 'article/article_create.html'
    form_class = ArticleForm
    success_message = 'Article created successfully'


    def form_valid(self, form):
        form.instance.authors = self.request.user
        return super().form_valid(form)


class ArticleUpdate(generic.edit.UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'article/article_update.html'

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        if self.object.authors != request.user:
            return redirect(self.object.get_absolute_url())
        return super().get(request, *args, **kwargs)


class ArticleDelete(generic.edit.DeleteView):
    model = Article
    template_name = 'article/article_confirm_delete.html'
    context_object_name = 'article'
    success_url = reverse_lazy('blog:article_list')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.authors != request.user:
            return redirect(self.object.get_absolute_url())
        return super().get(request, *args, **kwargs)


class ArticleSearch(ArticleListMixin):
    def get_queryset(self):
        try:
            queryset = Article.objects.annotate(search=SearchVector('title', 'text_body')).filter(search=self.request.GET['q'], active=True)
        except MultiValueDictKeyError: 
            queryset = super().get_queryset()  
        return queryset

    def get_context_data(self, *args, **kwargs):
        context =  super().get_context_data(*args, **kwargs)
        try:
            context['q'] = self.request.GET['q']
        except MultiValueDictKeyError:
            pass
        return context
