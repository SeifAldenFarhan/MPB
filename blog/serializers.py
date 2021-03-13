from django.contrib.auth.models import User
from rest_framework import serializers

from blog.models import Post, UserProfileInfo


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    username = UserSerializer()

    class Meta:
        model = UserProfileInfo
        fields = ['username']


class PostSerializer(serializers.HyperlinkedModelSerializer):
    author = UserSerializer()
    post_likes = UserSerializer(many=True)
    post_shares = UserSerializer(many=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'post_content', 'post_likes', 'post_shares', 'date']
