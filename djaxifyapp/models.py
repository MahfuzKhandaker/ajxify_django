from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField()

    objects = models.Manager()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    title = models.CharField(max_length=20)

    objects = models.Manager()

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(null=False, unique=True)
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail = models.ImageField()
    categories = models.ManyToManyField(Category)
    featured = models.BooleanField()
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    
    objects = models.Manager()
    
    class Meta: 
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['id'], name='id_index'),
        ]
 
    def __str__(self): 
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.slug})


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=1000)
    reply = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='replies', null=True, blank=True, default=None)
    post = models.ForeignKey(
        'Post', related_name='comments', on_delete=models.CASCADE)

    objects = models.Manager()

    class Meta: 
        ordering = ['-timestamp']

    def __str__(self):
        return '{}-{}'.format(self.post.title, str(self.user.username))