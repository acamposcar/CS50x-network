from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from .forms import PostForm, CommentForm
from .models import User, Post, Followers
from .utils import get_post, edit_post, delete_post, like_post, get_comments, create_comment, get_user, follow_user


def index(request):
    # Return posts in reverse chronological order
    posts = Post.objects.all().order_by("-timestamp")
    
    posts_paginator = Paginator(posts, 10)
    posts_page_number = request.GET.get('page')
    posts_page_obj = posts_paginator.get_page(posts_page_number)

    return render(request, "network/index.html", {
            "page_obj": posts_page_obj,
            "post_form": PostForm(),
            "comment_form": CommentForm(),
            })


def post(request, post_id):

    # Query for requested post
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "GET":
        return get_post(request, post)

    elif request.method == "PUT":
        return edit_post(request, post)

    elif request.method == 'DELETE':
        return delete_post(request, post)

    elif request.method == 'POST':
        return like_post(request, post)

    else:
        return JsonResponse({"error": "Method not allowed."}, status=400)

 
def comments(request, post_id):
    
    # Query for requested post
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "GET":
        return get_comments(request, post)
    
    elif request.method == "POST":
        return create_comment(request, post)

    else:
        return JsonResponse({"error": "Method not allowed."}, status=400)


def user_profile(request, username):

    try:   
        profile_user = User.objects.get(username = username)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)

    if request.method == "GET":
        return get_user(request, profile_user)
    
    elif request.method == "POST":
        return follow_user(request, profile_user)

    else:
        return JsonResponse({"error": "Method not allowed."}, status=400)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

        
@login_required(login_url=login_view)
def following_posts(request, username):

    try:   
        user = User.objects.get(username = username)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)
        
    # Get users followed by requested user
    users_following = Followers.objects.filter(user = user).values_list('following')
    
    # Return posts in reverse chronological order
    posts = Post.objects.filter(user__in=users_following).order_by("-timestamp")

    posts_paginator = Paginator(posts, 10)
    posts_page_number = request.GET.get('page')
    posts_page_obj = posts_paginator.get_page(posts_page_number)

    return render(request, "network/index.html", {
            "page_obj": posts_page_obj,
            "comment_form": CommentForm()
            })
            
@login_required(login_url=login_view)
def new_post(request):

    # Creating a new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    form = PostForm(request.POST)

    if form.is_valid():
        content = form.cleaned_data["content"]

        # Save post in database
        post = Post(user=request.user, content=content)
        post.save()

    return HttpResponseRedirect(reverse("index"))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")



