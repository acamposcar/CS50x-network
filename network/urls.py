
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts", views.all_posts, name="all_posts"),
    path("posts/<int:post_id>", views.post, name="post"),
    path("<str:username>", views.profile, name="profile"),
    path("<str:username>/posts", views.user_posts, name="user_posts"),
    path("<str:username>/following", views.following, name="following"),
    path("<str:username>/followers", views.followers, name="followers"),
    
]
