from django import forms
from django.contrib.auth.models import User
from django.core import validators
from django.core.exceptions import ValidationError
from .models import Post


# custom validator for checking password
def PasswordValidator(value):
    SpecialSym = ['$', '@', '#', '%', '&', '!', '^']
    if not any(char in SpecialSym for char in value):
        raise ValidationError("Password should have at least one of the symbols '$ @ # % & ! ^'")
    elif not any(char.isdigit() for char in value):
        raise ValidationError('Password should have at least one numeral')
    else:
        return value


# form for registration page
class UserInfoForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), validators=[PasswordValidator])

    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 'email')
        help_texts = {'username': None, }


# form for creating blogs
class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ('title', 'text')
