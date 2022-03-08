from xml.etree.ElementTree import Comment
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Likes, User, Post, Followers
from .views import login_view

import json

# Return all posts
def get_all_posts(request):

    posts = Post.objects.all()
    # Return posts in reverse chronologial order
    posts = posts.order_by("-timestamp").all()

    return JsonResponse([post.serialize() for post in posts], safe=False)


# Return all posts
def get_user_posts(request, username):

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
def get_post(request, post_id):

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
def get_profile(request, username):

    if request.user.username != username:
        return JsonResponse({"error": "Forbidden."}, status=403)

    # Query for requested user
    try:
        user = User.objects.get(username = username)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)

    return JsonResponse(user.serialize(), safe=False)


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
def new_post(request):

    # Creating a new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Get all request data
    data = json.loads(request.body)

    # Get contents
    image_url = data.get("image_url", "")
    content = data.get("content", "")
    if content == "":
        return JsonResponse({"error": "Content empty."}, status=400)

    # Save post in database
    post = Post(
        user=request.user,
        content=content,
        image_url=image_url,
    )
    post.save()

    return JsonResponse({"message": "Post created successfully."}, status=201)


@login_required(login_url=login_view)
def new_comment(request, post_id):

    # Creating a new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Get all request data
    data = json.loads(request.body)

    try:
        post = Post.objects.get(pk=post_id)
    except User.DoesNotExist:
        return JsonResponse({"error": f"Post with id {post_id} does not exist."}, status=400)

    # Get contents
    content = data.get("content", "")
    if content == "":
        return JsonResponse({"error": "Content empty."}, status=400)

    # Save post in database
    comment = Comment(
        user=request.user,
        content=content,
        post = post,
    )
    comment.save()

    return JsonResponse({"message": "Comment created successfully."}, status=201)
    

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


