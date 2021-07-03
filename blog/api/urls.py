from django.urls import path, re_path
from .views import postListAPIView, LikeToggleAPIView
from . import views


urlpatterns = [
    path('', postListAPIView.as_view(), name='blog-home'), #api/blog
    re_path(r'^(?P<pk>\d+)/like/$', LikeToggleAPIView.as_view(), name='like-toggle'),
    #path('', views.post_list, name='blog-home'),
    #path('post/<int:pk>/', views.post_detail, name='post-detail'),
    #path('post/new/', PostCreateView.as_view(), name='post-create'),
    #path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    #path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    #path('post/<int:pk>/postlikes/', views.post_likes, name='post-likes'),
    #path('about/', views.about, name='blog-about'),
    #path('connection/', followersView.as_view(), name='followers'),
    #re_path(r'^connect/(?P<operation>.+)/(?P<pk>\d+)/$', views.change_friends, name='change_friends')
]