from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexPageView.as_view(), name="index-page"),
    path("posts", views.AllPostsView.as_view(), name="posts-page"),
    path("posts/<slug:slug>", views.SinglePostView.as_view(), name="post-detail-page"), # /posts/post-name 
    path("unread", views.ReadLaterView.as_view(), name="unread")
]