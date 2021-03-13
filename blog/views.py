from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
from rest_framework import viewsets

from blog import models
from blog.forms import UserForm, UserInfoForm
from blog.serializers import PostSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class PostViewSet(viewsets.ModelViewSet):
    queryset = models.Post.objects.all().order_by('date')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]


@csrf_exempt
def user_logout(request):
    logout(request)
    return HttpResponse("User logged out")


@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponse("User Logged-in successfully.")
            else:
                return HttpResponseNotFound("Account Not Active!")
        else:
            return HttpResponseNotFound("Invalid login details!")
    else:
        return HttpResponseBadRequest("Bad Request.")


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
            data = "username: " + str(user_form['username'].value()) + \
                   ", email: " + str(user_form['email'].value()) + \
                   ", registered: " + str(registered)
            return HttpResponse(data)
        else:
            return HttpResponseBadRequest(f"User Exists Or Form Have Invalid Failed/s.")
    else:
        return HttpResponseBadRequest("Bad request.")


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
            return JsonResponse({"User": user_.username, "liked Post": post_.post_content})
        else:
            return HttpResponseNotFound("User or Post does not exist.")
    else:
        return HttpResponseBadRequest("Bad request.")


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
            return HttpResponse(f"User: {user_.username} shared Post: {post_.post_content}"
                                f"\nNew post created.")
        else:
            return HttpResponseNotFound("User or Post does not exist.")
    else:
        return HttpResponseBadRequest("Bad request!")


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
            return HttpResponse(f"User: {user_.username} unliked Post: {post_.post_content}")
        else:
            return HttpResponseNotFound("User or Post does not exist.")
    else:
        return HttpResponseBadRequest("Bad request!")


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
            return HttpResponse(f"New blog posted: {post_content}, Author: {user_.username}")
        else:
            return HttpResponseNotFound("User does not exist.")
    else:
        return HttpResponseBadRequest("Bad request.")


@csrf_exempt
def edit_post(request):
    if request.method == 'POST':
        user = request.user
        post_new_content = request.POST.get('new_content')
        post = request.POST.get('post_id')
        user_exist = models.User.objects.filter(username=user).count()
        post_ = models.Post.objects.get(pk=post)
        old_content = post_.post_content
        if user_exist > 0:
            if user.id == post_.author.id:
                post_.post_content = post_new_content
                post_.save()
                return HttpResponse(f"Blog edit: \nNew content - {post_new_content},\n"
                                    f"Old content - {old_content}")
            else:
                return HttpResponseNotAllowed(f"The user {user} can not edit this post.")
        else:
            return HttpResponseNotFound("User does not exist.")
    else:
        return HttpResponseBadRequest("Bad request.")


@csrf_exempt
def delete_post(request):
    if request.method == 'POST':
        user = request.user
        post = request.POST.get('post_id')
        user_exist = models.User.objects.filter(username=user).count()
        post_ = models.Post.objects.get(pk=post)
        if user_exist > 0:
            if post_:
                if user.id == post_.author.id:
                    post_content = post_.post_content
                    post_.delete()
                    return HttpResponse(f"Post '{post_content}' deleted")
                else:
                    return HttpResponseNotAllowed(f"The user {user} cannot delete this post."
                                                  f"\nThe author just can delete it.")
            else:
                HttpResponseNotFound("Post does not exist.")
        else:
            HttpResponseNotFound("User does not exist.")
    else:
        return HttpResponseBadRequest("Bad request!")
