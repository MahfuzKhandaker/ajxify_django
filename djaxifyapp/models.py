from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title           = models.CharField(max_length=125)
    slug            = models.SlugField(null=False, unique=True)
    summary         = models.CharField(max_length=255, null=True, blank=True)
    body            = models.TextField()
    created_on      = models.DateTimeField(auto_now_add=True)
    last_modified   = models.DateTimeField(auto_now=True)
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
