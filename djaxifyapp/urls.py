from django.urls import path
from djaxifyapp.views import JoinFormView, PostCreateView, PostListView, PostDetailView, likes

urlpatterns = [
    path('join/', JoinFormView.as_view()),
    path('', PostListView.as_view(), name='post-list'),
    path('likes/', likes, name='likes'),
    path('<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('create/', PostCreateView.as_view(), name='create-post')
]
