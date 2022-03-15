from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponseRedirect

from .forms import CommentForm, PostForm
from .models import User, Post, Followers, Likes, Comment

import json


"""
########
POST 
########
"""


def get_post(request, post):

    # Comment paginator object
    comments = Comment.objects.filter(post=post).order_by("-timestamp")
    comments_paginator = Paginator(comments, 10)
    comments_page_number = request.GET.get('page')
    comments_page_obj = comments_paginator.get_page(comments_page_number)

    return render(request, "network/post.html", {
        "post": post,
        "page_obj": comments_page_obj,
        "comment_form": CommentForm(),
        "post_form": PostForm(),
    })


def edit_post(request, post):

    # Request user must be the same as post author to be able to edit the post
    if request.user != post.user:
        return JsonResponse({"error": "Forbidden."}, status=403)

    # Loads data from JSON and gets post content
    data = json.loads(request.body)
    content = data.get("content", "")

    if content == "":
        return JsonResponse({"error": "Post empty."}, status=400)

    # Update post
    post.content = content
    post.save()

    return JsonResponse({"message": f"Post edited"}, status=200)


def delete_post(request, post):

    # Request user must be the same as post author to be able to edit the post
    if request.user != post.user:
        return JsonResponse({"error": "Forbidden."}, status=403)

    # Delete post
    post.delete()

    return JsonResponse({"message": f"Post deleted"}, status=200)


def like_post(request, post):

    if request.user.is_authenticated == False:
        return JsonResponse({"error": "Forbidden."}, status=403)

    like = Likes.objects.filter(user=request.user, post=post)

    if like.exists():
        like.delete()
    else:
        like = Likes(user=request.user, post=post)
        like.save()

    # Query for like count for current post
    like_count = Likes.objects.filter(post=post).count()

    return JsonResponse({"message": f"Liked post with id {post.id}", "like_count": like_count}, status=200)


"""
########
COMMENTS 
########
"""


def get_comments(request, post):

    comments = Comment.objects.filter(post=post).order_by('-timestamp')

    return JsonResponse([comment.serialize() for comment in comments], safe=False)


def create_comment(request, post):

    if request.user.is_authenticated == False:
        return JsonResponse({"error": "Forbidden."}, status=403)

    data = json.loads(request.body)

    # Get comment contents
    content = data.get("comment", "")

    if content == "":
        return JsonResponse({"error": "Comment empty."}, status=400)

    # Save comment in database
    comment = Comment(user=request.user, content=content, post=post)
    comment.save()

    # Query for comment count for current post
    comment_count = Comment.objects.filter(post=post).count()

    return JsonResponse({"message": f"Created comment", "comment_count": comment_count}, status=200)


"""
########
USER 
########
"""


def get_user(request, profile_user):

    # Query for users being followed by requested user
    users_following = Followers.objects.filter(
        user=profile_user).values_list('following')
    following_user_list = User.objects.filter(id__in=users_following)

    # Query for users who follow requested user
    users_followers = Followers.objects.filter(
        following=profile_user).values_list('user')
    followers_user_list = User.objects.filter(id__in=users_followers)

    # Return user posts in reverse chronological order
    posts = Post.objects.filter(user=profile_user).order_by("-timestamp").all()
    post_count = posts.count()

    post_paginator = Paginator(posts, 10)
    post_page_number = request.GET.get('page')
    post_page_obj = post_paginator.get_page(post_page_number)

    # Active item in navbar
    if profile_user == request.user:
        active = 'profile'
    else:
        active = ""

    return render(request, "network/profile.html", {
        "profile_user": profile_user,
        "page_obj": post_page_obj,
        'users_following': following_user_list,
        'users_followers': followers_user_list,
        "comment_form": CommentForm(),
        "post_form": PostForm(),
        "post_count": post_count,
        "active": active,

    })


def follow_user(request, profile_user):

    if request.user.is_authenticated == False:
        return JsonResponse({"error": "Forbidden."}, status=403)

    # Query for followers
    following = Followers.objects.filter(
        user=request.user, following=profile_user)

    if following.exists():
        following.delete()
    else:
        following = Followers(user=request.user, following=profile_user,)
        following.save()

    # Redirect to the place where the request came
    return HttpResponseRedirect(request.headers['Referer'])
