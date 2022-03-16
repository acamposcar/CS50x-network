from django.contrib import admin
from .models import User, Post, Likes, Followers, Comment

# Register your models here.
""" class Post(admin.ModelAdmin):
    list_display = ("__str__", "duration")

class PassengerAdmin(admin.ModelAdmin):
    filter_horizontal = ("flights",)
     """

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Likes)
admin.site.register(Followers)
admin.site.register(Comment)
