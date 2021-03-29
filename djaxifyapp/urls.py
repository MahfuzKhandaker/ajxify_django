from django.urls import path
from djaxifyapp.views import PostCreateView, post_list, post_detail,  favourite_post, post_favourite_list, likes


urlpatterns = [
    path('', post_list, name='post-list'),
    # path('posts_paginate/', posts_paginate, name='posts_paginate'),
    path('likes/', likes, name='likes'),
    path('favourites/', post_favourite_list, name='post_favourite_list'),
    path('<slug:slug>/', post_detail, name='post-detail'),
    path('<slug:slug>/favourite_post/', favourite_post, name='favourite_post'),
    path('create/', PostCreateView.as_view(), name='create-post'),
]