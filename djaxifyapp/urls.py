from django.urls import path
from djaxifyapp.views import PostCreateView, post_list, load_more_posts, post_detail,  favourite_post, post_favourite_list, likes


urlpatterns = [
    path('', post_list, name='post-list'),
    path('load_more_posts/', load_more_posts, name='load_more_posts'),
    path('likes/', likes, name='likes'),
    path('favourites/', post_favourite_list, name='post_favourite_list'),
    path('<slug:slug>/', post_detail, name='post-detail'),
    path('<slug:slug>/favourite_post/', favourite_post, name='favourite_post'),
    path('create/', PostCreateView.as_view(), name='create-post'),
]