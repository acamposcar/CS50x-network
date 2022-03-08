import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django import forms
from .models import User, Post, Followers, Likes, Comment

class NewPost(forms.Form):
    content = forms.CharField(widget=forms.Textarea(
        attrs={"placeholder": "¿What is going on?", "rows":5, "class":"form-control"}), required=True)
    image_url=forms.URLField(widget=forms.URLInput(
        attrs={"placeholder": "Image URL", "class":"form-control"}),  required=False)    

class NewComment(forms.Form):
    content = forms.CharField(widget=forms.Textarea(
        attrs={"placeholder": "Send your answer", "rows":5, "class":"form-control"}), required=True)


def index(request):
    # Return posts in reverse chronological order
    posts = Post.objects.all().order_by("-timestamp")
    
    return render(request, "network/index.html", {
            "posts": posts,
            "form": NewPost(),
            })

def user_posts(request, username):

    try:   
        user = User.objects.get(username = username)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)
        
    # Return posts in reverse chronological order
    posts = Post.objects.filter(user=user).order_by("-timestamp")

    return render(request, "network/index.html", {
            "posts": posts,
            "form": NewPost(),
            })


def following_view(request, username):

    try:   
        user = User.objects.get(username = username)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)
        
    # Get users followed by requested user
    users_following = Followers.objects.filter(user = user).values_list('following')
    
    # Return posts in reverse chronological order
    posts =Post.objects.filter(user__in=users_following).order_by("-timestamp")

    return render(request, "network/index.html", {
            "posts": posts,
            "form": NewPost(),
            })
            

def post_view(request, post_id):

    # Query for requested post
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return {"error": "Post not found.", "status": 404}
    
    comments = Comment.objects.filter(post=post)

    return render(request, "network/post.html", {
            "post": post,
            "comments": comments,
            "form": NewComment(),
            })

def user_profile(request, username):

    ## if request.user.username != username:
    ##     return JsonResponse({"error": "Forbidden."}, status=403)

    try:   
        user = User.objects.get(username = username)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)

    # Return user posts in reverse chronological order
    posts = Post.objects.filter(user=user).order_by("-timestamp").all()
    
    return render(request, "network/profile.html",{
            "user": user,
            "posts": posts
            })


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


@login_required(login_url=login_view)
def new_post(request):

    # Creating a new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    form = NewPost(request.POST)

    if form.is_valid():
        content = form.cleaned_data["content"]
        image_url = form.cleaned_data["image_url"]

        # Save post in database
        post = Post(
            user=request.user,
            content=content,
            image=image_url,
        )
        post.save()

    return HttpResponseRedirect(reverse("index"))


@login_required(login_url=login_view)
def new_comment(request, post_id):

    # Creating a new comment must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    form = NewComment(request.POST)

    # Query for requested post
    try:
        post = Post.objects.get(pk=post_id)
    except User.DoesNotExist:
        return JsonResponse({"error": f"Post with id {post_id} does not exist."}, status=400)

    if form.is_valid():
        content = form.cleaned_data["content"]

        # Save comment in database
        comment = Comment(
            user=request.user,
            content=content,
            post = post,
        )
        comment.save()

    # Redirect to the place where the request came
    return HttpResponseRedirect(request.headers['Referer'])


# Return all user posts
def get_user_posts(username):

    # Query for requested user
    try:
        user = User.objects.get(username = username)
    except User.DoesNotExist:
        return {"error": "User not found.", "status": 404}

    # Get all posts made by the user
    posts = Post.objects.filter(user = user)

    # Return posts in reverse chronological order
    posts = posts.order_by("-timestamp").all()

    return JsonResponse([post.serialize() for post in posts], safe=False)


# Return selected post
def get_post(request, post_id):

    # Query for requested post
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return {"error": "Post not found.", "status": 404}

    # Return post contents
    if request.method == "GET":
        return JsonResponse(post.serialize(), safe=False)
    else:
        return JsonResponse({"error": "GET request required."}, status=400)


def get_following(request, username):

    # Query for requested user
    try:
        user = User.objects.get(username = username)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)


    following = Followers.objects.filter(user = user)    

    return JsonResponse([user.serialize_following() for user in following], safe=False)


def get_followers(request, username):

    # Query for requested user
    try:
        user = User.objects.filter(username = username)
    except User.DoesNotExist: 
        return JsonResponse({"error": "User not found."}, status=404)

    followers = Followers.objects.filter(following__in=user)

    return JsonResponse([follower.serialize_followers() for follower in followers], safe=False)
    

@login_required(login_url=login_view)
def new_like(request, post_id):

    # Creating a new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Get all request data
    data = json.loads(request.body)

    try:
        post = Post.objects.get(pk=post_id)
    except User.DoesNotExist:
        return JsonResponse({"error": f"Post with id {post_id} does not exist."}, status=400)

    # Save post in database
    like = Likes(
        user=request.user,
        post = post,
    )
    like.save()

    return JsonResponse({"message": "Like created successfully."}, status=201)

