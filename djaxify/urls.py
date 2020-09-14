"""djaxify URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from djaxifyapp.views import JoinFormView, PostCreateView, PostListView, PostDetailView, likes

urlpatterns = [
    path('admin/', admin.site.urls),
    path('join/', JoinFormView.as_view()),
    path('blog/', PostListView.as_view(), name='post-list'),
    path('likes/', likes, name='likes'),
    path('blog/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('blog/create/', PostCreateView.as_view(), name='create-post')
]
