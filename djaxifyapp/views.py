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
from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
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
    template_name = 'post_list.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Post.published.all()
        paginator = Paginator(context['object_list'], 3)
        page_number = self.request.GET.get('page')
        context['page_obj'] = paginator.get_page(page_number)
        # try:
        #     context['object_list'] = paginator.page(page)
        # except PageNotAnInteger:
        #     context['object_list'] = paginator.page(1)
        # except EmptyPage:
        #     context['object_list'] = paginator.page(paginator.num_pages)
        
        return context
        


# def post_list(request):
#     post_list = Post.published.all()

#     #number of items on each page
#     number_of_item = 5
#     # Paginator
#     obj_paginator = Paginator(post_list, number_of_item)
#     #query_set for first page
#     first_page = obj_paginator.page(1).object_list
#     #range of page ex range(1, 3)
#     page_range = obj_paginator.page_range

#     context = {
#         # 'posts': post_list,
#         'obj_paginator':obj_paginator,
#         'first_page':first_page,
#         'page_range':page_range
#     }
#     if request.is_ajax():
#         page_n = request.POST.get('page_n', None) #getting page number
#         results = list(obj_paginator.page(page_n).object_list.values())
#         print(results)
#         return JsonResponse({'results':results})

#     return render(request, 'post_list.html', context )


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = Comment.objects.filter(post=post, reply=None).order_by('-id')
    
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True

    is_favourite = False
    if post.favourite.filter(id=request.user.id).exists():
        is_favourite = True

    if request.method=='POST':
        querydict = request.POST
        comment_form = CommentForm(querydict)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.reply_id = querydict.get('comment_id')
            comment.save()
    else:
        comment_form = CommentForm()
    
    context = {
        'post': post,
        'is_liked': is_liked,
        'is_favourite': is_favourite,
        'comments': comments,
        'total_likes': post.likes.count(),
        'total_comments': post.comments.count(),
        'comment_form': comment_form,
    }
    if request.is_ajax():
        html = render_to_string('comment_section.html', context, request=request)
        comments = serializers.serialize('json', list(comments), fields=('content', 'reply', 'post', 'user__username'))
        return JsonResponse({'form': html, 'comments': comments})

    return render(request, 'post_detail.html', context)

def post_favourite_list(request):
    user = request.user
    favourite_posts = user.favourite.all()
    context = {
        'favourite_posts': favourite_posts,
    }
    return render(request, 'post_favourite_list.html', context)

def favourite_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.favourite.filter(id=request.user.id).exists():
        post.favourite.remove(request.user)
    else:
        post.favourite.add(request.user)
    return HttpResponseRedirect(post.get_absolute_url())

def likes(request):
    post = get_object_or_404(Post, slug=request.POST.get('post_slug'))
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