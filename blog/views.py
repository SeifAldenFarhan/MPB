import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from blog import models
from blog.forms import UserForm, UserInfoForm
from blog.serializers import PostSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class PostViewSet(viewsets.ModelViewSet):
    queryset = models.Post.objects.all().order_by('date')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, ]


@login_required
@csrf_exempt
def user_logout(request):
    logout(request)
    data_set = dict(detail="User Logged Out")
    json_response = json.dumps(data_set)
    return HttpResponse(json_response)


@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                user_ = models.User.objects.get(username=username)
                data_set = dict(username=user_.username, email=user_.email)
                json_response = json.dumps(data_set)
                return HttpResponse(json_response)
            else:
                data_set = dict(detail="Account Not Active.")
                json_response = json.dumps(data_set)
                return HttpResponseNotFound(json_response)
        else:
            data_set = dict(detail="Invalid Login Details.")
            json_response = json.dumps(data_set)
            return HttpResponseNotFound(json_response)
    else:
        data_set = dict(detail="Bad Request.")
        json_response = json.dumps(data_set)
        return HttpResponseBadRequest(json_response)


@csrf_exempt
def register(request):
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        user_info_form = UserInfoForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            user_profile = user_info_form.save(commit=False)
            user_profile.user = user
            user_profile.save()
            registered = True
            data_set = dict(username=str(user_form['username'].value()), email=str(user_form['email'].value()),
                            registered=registered)
            json_response = json.dumps(data_set)
            return HttpResponse(json_response)
        else:
            data_set = dict(detail="User Exists Or Form Have Invalid Failed/s.")
            json_response = json.dumps(data_set)
            return HttpResponseBadRequest(json_response)
    else:
        data_set = dict(detail="Bad request.")
        json_response = json.dumps(data_set)
        return HttpResponseBadRequest(json_response)


@login_required
@csrf_exempt
def like_post(request):
    if request.method == 'POST':
        user = request.user
        post_id = request.POST.get('post_id')
        user_exist = models.User.objects.filter(username=user).count()
        post_exist = models.Post.objects.filter(pk=post_id).count()
        if user_exist > 0 and post_exist > 0:
            post_ = models.Post.objects.get(pk=post_id)
            user_ = models.User.objects.get(username=user)
            post_.post_likes.add(user_)
            data_set = dict(user=user_.username, post={
                "post_id": post_.id,
                "author": post_.author.username,
                "post_content": post_.post_content})
            json_response = json.dumps(data_set)
            return HttpResponse(json_response)
        else:
            json_response = json.dumps(dict(detail="User or Post does not exist."))
            return HttpResponseNotFound(json_response)
    else:
        json_response = json.dumps(dict(detail="Bad request."))
        return HttpResponseBadRequest(json_response)


@login_required
@csrf_exempt
def share_post(request):
    if request.method == 'POST':
        user = request.user
        post_id = request.POST.get('post_id')
        user_exist = models.User.objects.filter(username=user).count()
        post_exist = models.Post.objects.filter(pk=post_id).count()
        if user_exist > 0 and post_exist > 0:
            post_ = models.Post.objects.get(pk=post_id)
            user_ = models.User.objects.get(username=user)
            post_.post_shares.add(user_)
            new_shared_post = models.Post(author=user_, post_content=post_.post_content)
            new_shared_post.save()
            data_set = dict(user=user_.username,
                            shared_post={
                                "post_id": post_.id,
                                "author": post_.author.username,
                                "post_content": post_.post_content},
                            new_post={
                                "post_id": new_shared_post.id
                            })
            json_response = json.dumps(data_set)
            return HttpResponse(json_response)
        else:
            json_response = json.dumps(dict(detail="User or Post does not exist."))
            return HttpResponseNotFound(json_response)
    else:
        json_response = json.dumps(dict(detail="Bad request."))
        return HttpResponseBadRequest(json_response)


@login_required
@csrf_exempt
def unlike_post(request):
    if request.method == 'POST':
        user = request.user
        post_id = request.POST.get('post_id')
        user_exist = models.User.objects.filter(username=user).count()
        post_exist = models.Post.objects.filter(pk=post_id).count()
        if user_exist > 0 and post_exist > 0:
            post_ = models.Post.objects.get(pk=post_id)
            user_ = models.User.objects.get(username=user)
            post_.post_likes.remove(user_)
            data_set = dict(user=user_.username, post={
                "post_id": post_.id,
                "author": post_.author.username,
                "post_content": post_.post_content})
            json_response = json.dumps(data_set)
            return HttpResponse(json_response)
        else:
            json_response = json.dumps(dict(detail="User or Post does not exist."))
            return HttpResponseNotFound(json_response)
    else:
        json_response = json.dumps(dict(detail="Bad request."))
        return HttpResponseBadRequest(json_response)


@login_required
@csrf_exempt
def post_post(request):
    if request.method == 'POST':
        user = request.user
        post_content = request.POST.get('post_content')
        user_exist = models.User.objects.filter(username=user).count()
        if user_exist > 0:
            user_ = models.User.objects.get(username=user)
            new_post = models.Post(author=user_, post_content=post_content)
            new_post.save()
            data_set = dict(
                post_id=new_post.id,
                author=new_post.author.username,
                post_content=new_post.post_content)
            json_response = json.dumps(data_set)
            return HttpResponse(json_response)
        else:
            json_response = json.dumps(dict(detail="User does not exist."))
            return HttpResponseNotFound(json_response)
    else:
        json_response = json.dumps(dict(detail="Bad request."))
        return HttpResponseBadRequest(json_response)


@login_required
@csrf_exempt
def edit_post(request):
    if request.method == 'POST':
        user = request.user
        post_new_content = request.POST.get('new_content')
        post_id = request.POST.get('post_id')
        post_exist = models.Post.objects.filter(id=post_id).count()
        user_exist = models.User.objects.filter(username=user).count()
        if user_exist > 0 and post_exist > 0:
            post_ = models.Post.objects.get(pk=post_id)
            if user.id == post_.author.id:
                old_content = post_.post_content
                post_.post_content = post_new_content
                post_.save()
                data_set = dict(
                    post_id=post_.id,
                    author=post_.author.username,
                    new_post_content=post_.post_content,
                    old_post_content=old_content)
                json_response = json.dumps(data_set)
                return HttpResponse(json_response)
            else:
                json_response = json.dumps(dict(detail=f"The user {user} can not edit this post."))
                return HttpResponseNotAllowed(json_response)
        else:
            json_response = json.dumps(dict(detail="User Or Post does not exist."))
            return HttpResponseNotFound(json_response)
    else:
        json_response = json.dumps(dict(detail="Bad request."))
        return HttpResponseBadRequest(json_response)


@login_required
@csrf_exempt
def delete_post(request):
    if request.method == 'POST':
        user = request.user
        post_id = request.POST.get('post_id')
        post_exist = models.Post.objects.filter(id=post_id).count()
        user_exist = models.User.objects.filter(username=user).count()
        if user_exist > 0 and post_exist > 0:
            post_ = models.Post.objects.get(pk=post_id)
            if user.id == post_.author.id:
                post_id = post_.id
                author = post_.author.username
                post_content = post_.post_content
                post_.delete()
                data_set = dict(
                    post_id=post_id,
                    author=author,
                    post_content=post_content)
                json_response = json.dumps(data_set)
                return HttpResponse(json_response)
            else:
                data_set = dict(response=f"The user {user} is not the post's author.")
                json_response = json.dumps(data_set)
                return HttpResponseBadRequest(json_response, status=401)
        else:
            json_response = json.dumps(dict(detail="Post or User does not exist."))
            return HttpResponseNotFound(json_response)
    else:
        json_response = json.dumps(dict(detail="Bad request!"))
        return HttpResponseBadRequest(json_response)
