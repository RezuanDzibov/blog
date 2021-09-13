from django.utils.datastructures import MultiValueDictKeyError
from django import shortcuts
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView as BaseLoginView
from django.views.generic.base import View
from base.mixins import AddToContextMixin, UnLoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from . import forms
from django.views import generic
from . import models
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.postgres.search import SearchVector


User = get_user_model()


class LoginView(UnLoginRequiredMixin, BaseLoginView, AddToContextMixin):
    context_dict = {"section": "login"}
    form_class = forms.LoginForm


class RegisterCreateView(UnLoginRequiredMixin, SuccessMessageMixin, generic.edit.CreateView):
    form_class = forms.SignUpForm
    success_url = reverse_lazy("login")
    template_name = "registration/register.html"
    success_message = "You have successfully created an account. Now enter your username and password in the form below to log into your account."


class UserProfileListView(generic.list.ListView, AddToContextMixin):
    model = models.UserProfile
    paginate_by = 6
    template_name = "user_profile/user_profile_list.html"
    context_object_name = "user_profiles"
    context_dict = {"section": "users"}


class UserProfileView(generic.base.View):
    def get(self, request, username):
        context = {}
        user = shortcuts.get_object_or_404(User, username=username)
        if request.user.is_authenticated and request.user == user:
            context["section"] ="my_profile"
        user_profile = models.UserProfile.objects.get(user=user)
        context["user_profile"] = user_profile
        if user.articles:
            last_two_articles = user.articles.filter(active=True)[:2]
            context["last_two_articles"] = last_two_articles
            return shortcuts.render(request, "user_profile/user_profile.html", context)
        return shortcuts.render(request, "user_profile/user_profile.html", context)


class UserDataUpdateView(LoginRequiredMixin, generic.base.View):
    def get(self, request, username):
        user = shortcuts.get_object_or_404(User, username=username)
        user_profile = models.UserProfile.objects.get(user__username=username)
        user_form = forms.IncludeUserFieldsForm(instance=user)
        user_profile_form = forms.UserProfileForm(instance=user_profile)
        context = {"user_profile_form": user_profile_form, "user_form": user_form}
        return shortcuts.render(request, "user_profile/user_profile_update.html", context)

    def post(self, request, username):
        user_obj = shortcuts.get_object_or_404(User, username=username)
        user_profile_obj = models.UserProfile.objects.get(user__username=username)
        user_profile_form = forms.UserProfileForm(request.POST, request.FILES, instance=user_profile_obj)
        user_form = forms.IncludeUserFieldsForm(request.POST, instance=user_obj)
        if user_profile_form.is_valid() and user_form.is_valid():
            user_profile = user_profile_form.save(commit=False)
            user_profile.user = user_form.save()
            user_profile.save()
            messages.success(request, "Your profile is updated successfully")
            return shortcuts.redirect(reverse_lazy("user_account:profile", kwargs={"username": user_profile.user.username}))
        else:
            context = {"user_profile_form": user_profile_form, "user_form": user_form}
            return shortcuts.render(request, "user_profile/user_profile_update.html", context)


class UserProfileSearch(generic.list.ListView):
    model = models.UserProfile
    paginate_by = 6
    template_name = "user_profile/user_profile_list.html"
    context_object_name = "user_profiles"

    def get_queryset(self):
        try:
            queryset = models.UserProfile.objects.annotate(search=SearchVector("user__username", "user__first_name", "user__last_name", "user__email", "bio")).filter(search=self.request.GET["q"])
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


class AddSocialNetworkLink(LoginRequiredMixin, generic.edit.CreateView):
    model = models.SocialLink
    form_class = forms.SocialLinkForm
    template_name = "user_profile/add_soc_net_link.html"

    def get(self, request, *args, **kwargs):
            link = request.user.user_profile.social_links.filter(social_net_name=kwargs["soc_net_name"])
            if link.exists():
                return shortcuts.redirect(shortcuts.reverse("user_account:profile", args=[self.request.user.username]))
            return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user_profile = self.request.user.user_profile
        form.instance.social_net_name = self.kwargs["soc_net_name"]
        return super().form_valid(form)

    def get_success_url(self):
        self.success_url = reverse_lazy("user_profile:profile", args=[self.request.user.username])
        return super().get_success_url()


class DeleteSocialNetworkLink(LoginRequiredMixin, View):
    def get(self, request, soc_net_name, *args, **kwargs):
        link = request.user.user_profile.social_links.filter(social_net_name=soc_net_name)
        if link.exists():
            link.delete()
        return shortcuts.redirect(shortcuts.reverse("user_account:profile", args=[self.request.user.username]))
