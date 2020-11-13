from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import FormView, CreateView, ListView, DetailView
from django.views.generic.edit import FormMixin
from django.http import JsonResponse
from .forms import PostForm, CommentForm
from .models import Post, Comment
from .mixins import AjaxFormMixin
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.urls import reverse_lazy
try:
    from django.utils import simplejson as json
except ImportError:
    import json


# class JoinFormView(AjaxFormMixin, FormView):
#     form_class = JoinForm
#     template_name  = 'forms/ajax.html'
#     success_url = '/form-success/'


class PostCreateView(AjaxFormMixin, CreateView):
    form_class = PostForm
    template_name = 'create_post.html'



class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'post_list.html'  


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    # comments = Comment.objects.filter(post=post, parent=None).order_by('-id')
    
    if request.method=='POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            if not request.user.is_authenticated:
                return redirect('login')

            content_data = comment_form.cleaned_data['content']
            parent_obj = None
            try:
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None

            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists():
                    parent_obj = parent_qs.first()

            new_comment, created = Comment.objects.get_or_create(
                post=post, 
                user=request.user,
                content=content_data,
                parent=parent_obj
            )
            return HttpResponseRedirect(new_comment.post.get_absolute_url())
    else:
        comment_form = CommentForm()
    
        
    

    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True


    context = {
        'post': post,
        'is_liked': is_liked,
        'comments': post.comments.all(),
        'total_likes': post.likes.count(),
        'total_comments': post.comments.count(),
        'comment_form': comment_form,
    }
    # if request.is_ajax():
    #     html = render_to_string('comment_section.html', context, request=request)
    #     return JsonResponse({'form': html})

    return render(request, 'post_detail.html', context)


def likes(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    context ={
        'post': post,
        'is_liked': is_liked,
        'total_likes': post.likes.count(),
    }
    if request.is_ajax():
        html = render_to_string('like_section.html', context, request=request)
        return JsonResponse({'form': html})
    # return HttpResponseRedirect(post.get_absolute_url())