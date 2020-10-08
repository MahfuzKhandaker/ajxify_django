from django.urls import path
from djaxifyapp.views import JoinFormView, PostCreateView, PostListView, PostDetailView, AddCommentView, likes

urlpatterns = [
    path('join/', JoinFormView.as_view()),
    path('', PostListView.as_view(), name='post-list'),
    path('likes/', likes, name='likes'),
    path('<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('create/', PostCreateView.as_view(), name='create-post'),
    path('<slug:slug>/comment', AddCommentView.as_view(), name='add-comment'),
]
