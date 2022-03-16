
from lib2to3.pgen2.pgen import DFAState
from django.contrib.auth.models import AbstractUser
from django.db import models
import random

THE_OFFICE_PROFILE = [
    'https://socialnewsdaily.com/wp-content/uploads/2018/07/rsz_014.jpg',
    'https://images.thebrag.com/tb/uploads/2020/02/PAMHEAD-768x437.jpg',
    'https://www.cultture.com/pics/2021/06/the-office-10-teorias-de-los-fans-que-tienen-demasiado-sentido-0.jpg',
    'https://1.bp.blogspot.com/-TAjlxuqoAp8/XoTJpp1mTzI/AAAAAAAAJJk/_rKTvsvfin8Vt-xPU0n9j34I7okTLxH8gCEwYBhgLKs4DAMBZVoCctLm-dNK578kFojA_mIdN7nkfwLLDI6cVlXxLlsm3VuEgx1fw8P6O3fKPS_K-LICzkVqfNyZ83I3qu76aMZjSTcQneQ4NYnXpW6Q5wHEWPh1QMByjRItTDWuSojpJ2uL31JZ4UuYILdsHxpNfjxoJAj7JqgSaYITgmjLOqeSoNg0ZQYiD3iusn_v5QOyczrkSaENG8cd_R5b7o8uHIhoNvaAncorSddQYAAb9j4SPW8rca6sL3Y1M5rUd6KTSsfoRKONeDlRdsYR6DzSGbs5oE3LLCK-alU-5n1WREwU8xqQtY4l8JBrP-mndGGPTi5Lt1CJGTwofESEfcrQu4NBhWKcROL4wnhX6w1vTGfc0EH_Z62KutfOok0anCJd1h53M2zy-YJDg7n5H-vPMm_9ihJ5r-RLRVgkdS1-Wkl6zJDTSP2LZ9vdydt8ZDPkcIyj8w2EcVH3m4TFBkaOnW44YqCYgbJVX7bSK2X4ULSMKQrfpJasHE_F5uIFRwhiE8KVkWn8_GO9Ngp5u7wFEnY4xVwlKKNLwfG8yAub3haeP90qJvHgdR2A1lJ0uj-SUhcmMYcovhJ1aAN_Hdz-M3STEUTT927KL_1YFMPOok_QF/s640/the-office-brian-500x279.jpg',
    'https://poptv.orange.es/wp-content/uploads/sites/3/2020/08/phyllis-smith.jpg',
    'https://www.ecartelera.com/images/sets/43800/43814.jpg',
    'https://www.ecartelera.com/images/sets/43800/43825.jpg'
]


class User(AbstractUser):
    profile_image = models.URLField(
        default="https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/OOjs_UI_icon_userAvatar.svg/240px-OOjs_UI_icon_userAvatar.svg.png")

    def set_profile_image(self):
        self.profile_image = random.choice(THE_OFFICE_PROFILE)


class Post(models.Model):
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.URLField(default='', blank=True)

    def users_likes(self):
        user_likes_list = Likes.objects.filter(post=self).values_list('user')
        return User.objects.filter(id__in=user_likes_list)

    def last_comments(self):
        return Comment.objects.filter(post=self).order_by('-timestamp')[:3]

    def __str__(self):
        return f"Post [{self.id}] made by {self.user.username} on {self.timestamp.strftime('%d %b %Y %H:%M:%S') }"


class Comment(models.Model):
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="user_comments")
    post = models.ForeignKey(
        "Post", on_delete=models.CASCADE, related_name="comments", blank=True)
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
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="user_likes")
    post = models.ForeignKey(
        "Post", on_delete=models.CASCADE, related_name="likes", blank=True, null=True)

    class Meta:
        unique_together = ['user', 'post']

    def __str__(self):
        return f"{self.user} likes {self.post}"


class Followers(models.Model):
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="user_followers")
    following = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="user_following", blank=True, null=True)

    class Meta:
        unique_together = ['user', 'following']

    def __str__(self):
        return f"{self.user} is following {self.following}"
