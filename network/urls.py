
from django.urls import path

from . import views
from . import api

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts/<int:post_id>", views.post_view, name="post_view"),
    path("api/posts/<int:post_id>/edit", views.edit_post, name="edit_post"),
    path("api/posts/<int:post_id>/new_comment", views.new_comment, name="new_comment"),
    path("api/posts/<int:post_id>/new_like", views.new_like, name="new_like"),
    path("api/posts/<int:post_id>/comments", views.get_comments, name="get_comments"),
    path("api/new_post", views.new_post, name="new_post"),
    path("users/<str:username>", views.user_profile, name="user_profile"),
    path("users/<str:username>/posts", views.user_posts, name="user_posts"),
    path("users/<str:username>/following", views.following_posts, name="following_posts"),
    path("api/users/<str:username>/new_follow", views.new_follow, name="new_follow"),


    
]
