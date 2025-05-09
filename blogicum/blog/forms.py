from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Post, Comment


User = get_user_model()


class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class ProfileEditForm(UserChangeForm):
    password = None
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'pub_date', 'location', 'category', 'image']
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
        }
