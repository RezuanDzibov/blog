from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth import get_user_model
from .models import UserProfile, SocialLink
from django.contrib.auth.forms import AuthenticationForm, UsernameField

User = get_user_model()


class LoginForm(AuthenticationForm):
    username = UsernameField(label="Username or Email", widget=forms.TextInput(attrs={"autofocus": True}))


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "type": "text"}),
            "first_name": forms.TextInput(attrs={"class": "form-control", "type": "text"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "type": "text"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "type": "text"}),
        }

    def clean(self):
        cd = super(SignUpForm, self).clean()
        email = cd.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with the same email address already exists.")


class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields = ("bio", "avatar")
        widgets = {
            "bio": forms.Textarea(attrs={"class": "form-control", "id": "exampleFormControlTextarea1"}), 
            "avatar": forms.FileInput(attrs={"class": "form-control", "id": "Formfile", "type": "file"})
        }

class IncludeUserFieldsForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ("first_name", "last_name")
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control", "type": "text"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "type": "text"}),
        }


class SocialLinkForm(forms.ModelForm):

    class Meta:
        model = SocialLink
        fields = ("url",)