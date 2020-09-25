from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    STATUS_CHOICES  = (
        ('draft','Draft'),
        ('published','Published'),
    )
    title           = models.CharField(max_length=125)
    slug            = models.SlugField(null=False, unique=True)
    author          = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    summary         = models.CharField(max_length=255, null=True, blank=True)
    body            = models.TextField()
    created_on      = models.DateTimeField(auto_now_add=True)
    last_modified   = models.DateTimeField(auto_now=True)
    status          = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    likes           = models.ManyToManyField(User, blank=True, related_name='likes')


    objects         = models.Manager()

    class Meta: 
        ordering = ['-created_on']
        indexes = [
            models.Index(fields=['id'], name='id_index'),
        ]
 
    def __str__(self): 
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=250)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return '{}-{}'.format(self.post.title, str(self.user.username))
        