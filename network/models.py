import email
from lib2to3.pgen2.pgen import DFAState
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    profile_image = models.URLField(default="https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/OOjs_UI_icon_userAvatar.svg/240px-OOjs_UI_icon_userAvatar.svg.png")

    def serialize(self):

        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "image": self.profile_image,
        }

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.URLField(default='', blank=True)

    def serialize(self):

        return {
            "id": self.id,
            "user": self.user.username,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "image": self.image,
            "comments":  [comment.serialize() for comment in Comment.objects.filter(post=self)],
            "likes": [like.serialize() for like in Likes.objects.filter(post=self)]
        }

    def __str__(self):
        return f"Post {self.id}"


class Comment(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_comments")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="post_comments", blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        
        return {
            "id": self.id,
            "user": self.user.username,
            "post": self.post.id,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }

    def __str__(self):
        return f"Comment {self.content}"


class Likes(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_likes")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="posts_likes", blank=True, null=True)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "post": self.post.id,
        }

    def __str__(self):
        return f"{self.user} likes {self.post}"


class Followers(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_followers")
    following = models.ManyToManyField("User", related_name="user_following", blank=True)

    def serialize_followers(self):
        return {
            "id": self.id,
            "followers": self.user.username,
        }
    
    def serialize_following(self):
        return {
            "id": self.id,
            "following": [user.username for user in self.following.all()],
        }

    def __str__(self):
        return f"{self.user} is following.."