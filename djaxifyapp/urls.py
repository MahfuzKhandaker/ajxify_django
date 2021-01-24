from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from djaxifyapp.views import PostCreateView, PostListView, post_detail,  favourite_post, post_favourite_list, likes


urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('likes/', likes, name='likes'),
    path('favourites/', post_favourite_list, name='post_favourite_list'),
    path('<slug:slug>/', post_detail, name='post-detail'),
    path('<slug:slug>/favourite_post/', favourite_post, name='favourite_post'),
    path('create/', PostCreateView.as_view(), name='create-post'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
