from django import forms
from .models import Post, Comment


class JoinForm(forms.Form):
    email = forms.EmailField()
    name = forms.CharField(max_length=120)


class PostForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={
        'placeholder': 'Write your blog here...',
        'required': False, 
        'cols': 30, 
        'rows': 10
    })
    )

    class Meta:
        model = Post
        fields = ('title', 'slug', 'overview', 'content', 'thumbnail', 
        'categories', 'featured')


# class CommentForm(forms.Form):
#     # parent_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
#     content = forms.CharField(label='', widget=forms.Textarea(
#         attrs={
#             "class": "form-control",
#             "placeholder": "Leave a comment!",
#             "rows": "5"
#         })
#     )
class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Leave a comment!',
        'id': 'usercomment',
        'rows': '4'
    }))
    class Meta:
        model = Comment
        fields = ['content', ]