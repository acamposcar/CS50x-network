from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import User, Post, Followers


def index(request):
    return render(request, "network/index.html")


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

# Return all posts
def all_posts(request):

    posts = Post.objects.all()
    # Return posts in reverse chronologial order
    posts = posts.order_by("-timestamp").all()

    return JsonResponse([post.serialize() for post in posts], safe=False)


# Return all posts
def user_posts(request, username):

    # Query for requested user
    try:
        user = User.objects.get(username = username)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)

    # Get all posts made by the user
    posts = Post.objects.filter(user = user)

    # Return posts in reverse chronologial order
    posts = posts.order_by("-timestamp").all()

    return JsonResponse([post.serialize() for post in posts], safe=False)


# Return selected post
def post(request, post_id):

    # Query for requested post
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Return post contents
    if request.method == "GET":
        return JsonResponse(post.serialize(), safe=False)
    else:
        return JsonResponse({"error": "GET request required."}, status=400)


@login_required(login_url=login_view)
def profile(request, username):

    if request.user.username != username:
        return JsonResponse({"error": "Forbidden."}, status=403)

    # Query for requested user
    try:
        user = User.objects.get(username = username)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)

    return JsonResponse(user.serialize(), safe=False)


def following(request, username):

    # Query for requested user
    try:
        user = User.objects.get(username = username)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)

    following = Followers.objects.get(user = user)

    return JsonResponse(following.serialize_following(), safe=False)


def followers(request, username):

    # Query for requested user
    try:
        user = User.objects.filter(username = username)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)

    followers = Followers.objects.filter(following__in=user)

    return JsonResponse([follower.serialize_followers() for follower in followers], safe=False)