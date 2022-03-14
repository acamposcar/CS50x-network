import email
from lib2to3.pgen2.pgen import DFAState
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    profile_image = models.URLField(default="https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/OOjs_UI_icon_userAvatar.svg/240px-OOjs_UI_icon_userAvatar.svg.png")


class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.URLField(default='', blank=True)

    def users_likes(self):
        user_likes_list = Likes.objects.filter(post=self).values_list('user')
        return User.objects.filter(id__in = user_likes_list)

    def last_comments(self):
        return Comment.objects.filter(post=self).order_by('-timestamp')[:3]

    def __str__(self):
        return f"Post [{self.id}] made by {self.user.username} on {self.timestamp.strftime('%d %b %Y %H:%M:%S') }"


class Comment(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_comments")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="comments", blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.user.username,
            "profile_image": self.user.profile_image,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "post": self.post.id,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
        }
    def __str__(self):
        return f"Comment [{self.id}] made by {self.user.username} on {self.timestamp.strftime('%d %b %Y %H:%M:%S')}"


class Likes(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_likes")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="likes", blank=True, null=True)

    class Meta:
        unique_together = ['user', 'post']

    def __str__(self):
        return f"{self.user} likes {self.post}"


class Followers(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_followers")
    following = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_following", blank=True, null=True)
    
    class Meta:
        unique_together = ['user', 'following']

    def __str__(self):
        return f"{self.user} is following {self.following}"