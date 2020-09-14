from django import forms
from .models import Post


class JoinForm(forms.Form):
    email = forms.EmailField()
    name = forms.CharField(max_length=120)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'summary', 'body', 'likes',]
