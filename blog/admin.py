from django.contrib import admin
from .models import post, Comment, UserProfile
# Register your models here.

admin.site.register(post)

admin.site.register(UserProfile)

admin.site.register(Comment)