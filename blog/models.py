from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, )

    def __str__(self):
        return self.user.username


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='post_author')
    post_content = models.CharField(max_length=1000)
    post_likes = models.ManyToManyField(User, default=False, null=True, blank=True, related_name='likes')
    post_shares = models.ManyToManyField(User, default=False, null=True, blank=True, related_name='shares')
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return "post" + str(self.id)


class Comments(models.Model):
    comment_content = models.CharField(max_length=150)
    author = models.ForeignKey('UserProfileInfo', related_name='commenter', on_delete=models.CASCADE)
    commented_post = models.ForeignKey('Post', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author
