from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token
