from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from djaxifyapp.views import PostCreateView, PostListView, post_detail, likes


urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('likes/', likes, name='likes'),
    path('<slug:slug>/', post_detail, name='post-detail'),
    # path('add_comment/', add_comment, name='add_comment'),
    path('create/', PostCreateView.as_view(), name='create-post'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
