
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts/<int:post_id>", views.post, name="post"),
    path("posts/<int:post_id>/comments", views.comments, name="comments"),
    path("new_post", views.new_post, name="new_post"),
    path("users/<str:username>", views.user_profile, name="user_profile"),
    path("users/<str:username>/following",
         views.following_posts, name="following_posts"),
]
