
from django.urls import path

from . import views
from . import api

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("api/posts", api.get_all_posts, name="get_all_posts"),
    path("api/posts/<int:post_id>", api.get_post, name="get_post"),
    path("api/<str:username>", api.get_profile, name="get_profile"),
    path("api/<str:username>/posts", api.get_user_posts, name="get_user_posts"),
    path("api/<str:username>/following", api.get_following, name="get_following"),
    path("api/<str:username>/followers", api.get_followers, name="get_followers"),
    path("api/new_post", api.create_post, name="new_post"),
    path("api/posts/<int:post_id>/new_comment", api.create_post, name="new_comment"),
    path("api/posts/<int:post_id>/new_like", api.new_like, name="new_like"),
    
]
