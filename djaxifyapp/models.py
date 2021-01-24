from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify


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

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status="published")

class Post(models.Model):
    objects     = models.Manager()      #Default Manager
    published   = PublishedManager()  #Custom Model Manager

    STATUS_CHOICES = (
        ('draft','Draft'),
        ('published','Published'),
    )

    title       = models.CharField(max_length=100)
    slug        = models.SlugField(null=False, unique=True)
    overview    = models.TextField()
    timestamp   = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    content     = models.TextField()
    author      = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail   = models.ImageField()
    categories  = models.ManyToManyField(Category)
    featured    = models.BooleanField()
    status      = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    likes       = models.ManyToManyField(User, blank=True, related_name='likes')
    favourite   = models.ManyToManyField(User, related_name='favourite', blank=True)
    
    
    class Meta: 
        ordering = ['-id']
 
    def __str__(self): 
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.slug})

@receiver(pre_save, sender=Post)
def pre_save_slug(sender, **kwargs):
    slug = slugify(kwargs['instance'].title)
    kwargs['instance'].slug = slug


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(null=True, blank=True)
    photo = models.ImageField(null=True, blank=True)


    def __str__(self):
        return "Profile of user {}".format(self.user.username)

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