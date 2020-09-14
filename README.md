# ajxify_django
## how we can create likes function using django and ajax?
Here I am using ajax post response to make a django blog post like and dislike button functionality without refresh page loading.

## What is AJAX?
AJAX is Asynchronous JavaScript And XML, which is combination of browser built-in XMLHttpRequest object and Javascript and HTML DOM.

## Why we use ajax?
Many of the time we want to perform some asynchronous calls to the server to GET or POST some sort of data without refreshing your current page.

## in models.py
```python
class Post(models.Model):
      likes = models.ManyToManyField(User, blank=True, related_name='likes')
```
## urls.py

```python
from django.contrib import admin
from django.urls import path
from djaxifyapp.views import JoinFormView, PostCreateView, PostListView, PostDetailView, likes

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', PostListView.as_view(), name='post-list'),
    path('likes/', likes, name='likes'),
    path('blog/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
]

```

## in views.py

```python
class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'post_list.html'  
    
    
class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'post_detail.html'


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
```

## like_section.html

```python
{{ total_likes }} Like {{ total_likes|pluralize }}

{% if request.user.is_authenticated %}
<form action="{% url 'likes' %" method="POST">
    {% csrf_token %}
    {% if is_liked %}
        <button type="submit" id="like" name="post_id" value="{{ post.id }}" class="btn btn-danger">Dislike</button>
    {% else %}
        <button type="submit" id="like" name="post_id" value="{{ post.id }}" class="btn btn-primary">Like</button>
    {% endif %}
</form>
{% endif %}
```

## in post_detail.html

```python
<div id="like-section">
    {% include 'like_section.html' %}
</div>
```

## in base.html
create ajax post response using jquery

```js
$(document).ready(function(){
  $(document).on('click', '#like', function(event){
    event.preventDefault();
    var pk = $(this).attr('value');
    $.ajax({
      type: 'POST',
      url: '{% url "likes" %}',
      data: {
            'post_id': pk,
            'csrfmiddlewaretoken': '{{ csrf_token }}'
            },
            success: function(response){
              $('#like-section').html(response['form'])
            },
            error: function(rs, e){
              console.log(rs.responseText);
            },
          });
     });
})
```
