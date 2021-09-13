from django.shortcuts import redirect
from django.views import generic
from blog.models import Article
from django.contrib import messages


class ArticleListMixin(generic.list.ListView):
	template_name = "article/article_list.html"
	model = Article
	paginate_by = 4
	context_object_name = "articles"


class ErrorMessageMixin:
	error_message = ""

	def form_invalid(self, form):
		response = super().form_valid(form)
		error_message = self.error_message(form.cleaned_data)
		if error_message:
			messages.error(self.request, error_message)

	def get_error_message(self, cleaned_data):
		return self.error_message % cleaned_data


class WarningMessageMixin:
	warning_message = ""

	def form_invalid(self, form):
		response = super().form_valid(form)
		warning_message = self.get_warning_message(form.cleaned_data)
		if warning_message:
			messages.error(self.request, warning_message)

	def get_warning_message(self, cleaned_data):
		return self.warning_message % cleaned_data
	

class AddToContextMixin(generic.base.ContextMixin):
	context_dict = {}
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		for key, value in self.context_dict.items():
			context[f"{key}"] = value
		return context
	
class UnLoginRequiredMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("blog:article_list")
        return super().dispatch(request, *args, **kwargs)


class IsOwnerOrRedirect:
	owner_field_name = ""

	def get(self, request, *args, **kwargs):
		super().get(request, *args, **kwargs)
		if getattr(self.object, self.owner_field_name) != request.user:
			return redirect(self.object.get_absolute_url())
		return super().get(request, *args, **kwargs)
