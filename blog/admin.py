from django.contrib import admin

# Register your models here.
from blog.models import UserProfileInfo, Post, Comments

admin.site.register(UserProfileInfo)
admin.site.register(Post)
admin.site.register(Comments)
