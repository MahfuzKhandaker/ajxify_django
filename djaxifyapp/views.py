from django.shortcuts import render, get_object_or_404, reverse
from django.views.generic import FormView, CreateView, ListView, DetailView
from django.http import JsonResponse
from .forms import JoinForm, PostForm, CommentForm
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


class JoinFormView(AjaxFormMixin, FormView):
    form_class = JoinForm
    template_name  = 'forms/ajax.html'
    success_url = '/form-success/'


class PostCreateView(AjaxFormMixin, CreateView):
    form_class = PostForm
    template_name = 'create_post.html'



class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'post_list.html'  


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'post_detail.html'
    # form = CommentForm()

    # def get_object(self):
    #     obj = super().get_object()
    #     if self.request.user.is_authenticated:
    #         Comment.objects.get_or_create(
    #             user=self.request.user,
    #             post=obj
    #         )
    #     return obj


    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)
        post = get_object_or_404(Post, slug=self.kwargs['slug'])
        context['comments'] = post.comments.order_by('-timestamp')
        context['total_likes'] = post.likes.count()
        return context 


class AddCommentView(CreateView):
    form_class = CommentForm
    template_name = 'add_comment.html'

    def get_success_url(self):
        return reverse('post_detail', kwargs={'slug': self.object.post.slug})


    def form_valid(self, form):
        form.instance.post = Post.objects.get(slug=self.kwargs.get("slug"))
        form.instance.user = self.request.user
        return super().form_valid(form)

    success_url = reverse_lazy(get_success_url)


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