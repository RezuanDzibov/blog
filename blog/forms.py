from django import forms
from .models import Article, Comment
from ckeditor.widgets import CKEditorWidget


class ArticleForm(forms.ModelForm):
    
    text_body = forms.CharField(widget=CKEditorWidget)

    class Meta: 
        model = Article
        fields = ('title', 'text_body', 'category', 'tags', 'image', 'active')
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control', 'id': 'Formfile', 'type': 'file'})
        }

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text_body',)
        widgets = {'text_body': forms.Textarea(attrs={'class': 'form-control', 'id': 'exampleFormControlTextarea1', 'rows': '3'})}
        
