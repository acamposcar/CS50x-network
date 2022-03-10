from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django import forms
from django.core.paginator import Paginator
from .models import User, Post, Followers, Likes, Comment
from django.views.decorators.csrf import csrf_exempt
import json 

class NewPost(forms.Form):
    content = forms.CharField(widget=forms.Textarea(
        attrs={'autofocus': 'autofocus', "placeholder": "¿What is going on?", "rows":3, "class":"form-control"}), required=True)   

class NewComment(forms.Form):
    content = forms.CharField(widget=forms.Textarea(
        attrs={"placeholder": "Send your answer", "rows":1, "class":"form-control"}), required=True)


def index(request):
    # Return posts in reverse chronological order
    posts = Post.objects.all().order_by("-timestamp")
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
            "page_obj": page_obj,
            "post_form": NewPost(),
            "comment_form": NewComment()
            })

def user_posts(request, username):

    try:   
        user = User.objects.get(username = username)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)
        
    # Return posts in reverse chronological order
    posts = Post.objects.filter(user=user).order_by("-timestamp")

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
            "page_obj": page_obj,
            "form": NewPost(),
            })


def get_comments(request, post_id):
    
    # Query for requested post
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    comments = Comment.objects.filter(post=post).order_by('-timestamp')

    # Return post contents
    if request.method == "GET":
        return JsonResponse([comment.serialize() for comment in comments], safe=False)
    else:
        return JsonResponse({"error": "GET request required."}, status=400)


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
    posts =Post.objects.filter(user__in=users_following).order_by("-timestamp")

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
            "page_obj": page_obj,
            "post_form": NewPost(),
            "comment_form": NewComment()
            })
            

def post_view(request, post_id):

    # Query for requested post
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    comments = Comment.objects.filter(post=post).order_by("-timestamp")

    paginator = Paginator(comments, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/post.html", {
            "post": post,
            "page_obj": page_obj,
            "form": NewComment(),
            })

def user_profile(request, username):

    ## if request.user.username != username:
    ##     return JsonResponse({"error": "Forbidden."}, status=403)

    try:   
        profile_user = User.objects.get(username = username)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)

    # Query for users being followed by requested user
    users_following = Followers.objects.filter(user = profile_user).values_list('following')

    # Query for users who follow requested user
    users_followers = Followers.objects.filter(following = profile_user).values_list('user')

    following_user_list = User.objects.filter(id__in=users_following)
    followers_user_list = User.objects.filter(id__in=users_followers)
    # Return user posts in reverse chronological order

    posts = Post.objects.filter(user=profile_user).order_by("-timestamp").all()
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request, "network/profile.html",{
            "profile_user": profile_user,
            "page_obj": page_obj,
            'users_following': following_user_list,
            'users_followers': followers_user_list
            })


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

        # Save post in database
        post = Post(
            user=request.user,
            content=content,
        )
        post.save()

    return HttpResponseRedirect(reverse("index"))

@login_required(login_url=login_view)
def edit_post(request, post_id):
    # Query current post
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Request user must be the same as post author to be able to edit the post
    if request.user != post.user:
        return JsonResponse({"error": "Forbidden."}, status=403)

    # Edit post must be via PUT
    if request.method == "POST":
        
        form = NewPost(request.POST)

        if form.is_valid():
            content = form.cleaned_data["content"]

            # Update post
            post.content = content
            post.save()

        return HttpResponseRedirect(reverse("post_view", kwargs={"post_id": post_id}))
    
    elif request.method == 'GET':

        return render(request, "network/edit.html", {
                "form": NewPost(initial={'content': post.content}),
                "post": post
            })
    else:
        return JsonResponse({"error": "PUT or GET request required."}, status=400)
    

@csrf_exempt   
@login_required(login_url=login_view)
def new_comment(request, post_id):

    # Creating a new comment must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Query for requested post
    try:
        post = Post.objects.get(pk=post_id)
    except User.DoesNotExist:
        return JsonResponse({"error": f"Post with id {post_id} does not exist."}, status=400)

    data = json.loads(request.body)

    # Get contents of email
    content = data.get("comment", "")
    if content == [""]:
        return JsonResponse({
            "error": "Comment empty."
        }, status=400)

    # Save comment in database
    comment = Comment(
        user=request.user,
        content=content,
        post = post,
    )
    comment.save()

    comment_count = Comment.objects.filter(post=post).count()
    # Redirect to the place where the request came
    return JsonResponse({"message": f"Created comment", "comment_count": comment_count}, status=200)

@csrf_exempt   
@login_required(login_url=login_view)
def new_like(request, post_id):

    # Creating a new like must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    # Query for requested post
    try:
        post = Post.objects.get(pk=post_id)
    except User.DoesNotExist:
        return JsonResponse({"error": f"Post with id {post_id} does not exist."}, status=400)

    # Query for like by current user
    like = Likes.objects.filter(user=request.user, post=post)

    if like.exists():
        # Delete like from database
        like.delete()
    else:
        # Save like in database
        like = Likes(
            user=request.user,
            post = post,
            )
        like.save()

    # Query for like count for current post
    like_count = Likes.objects.filter(post=post).count()

    # Redirect to the place where the request came
    return JsonResponse({"message": f"Liked post with id {post_id}", "like_count": like_count}, status=200)


@login_required(login_url=login_view)
def new_follow(request, username):

    # Creating a new like must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    # Query for requested user
    try:   
        following_user = User.objects.get(username = username)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)

    # Query for requested like
    following = Followers.objects.filter(user=request.user, following=following_user)

    if following.exists():
        # Delete like from database
        following.delete()
    else:
        # Save like in database
        following = Followers(
            user = request.user,
            following = following_user,
            )
        following.save()

    # Redirect to the place where the request came
    return HttpResponseRedirect(request.headers['Referer'])
