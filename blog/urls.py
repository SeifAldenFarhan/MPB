from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from blog import views

router = routers.DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'users', views.UserViewSet)

# router.routes(r'likepost', views.like_post, 'like_post')
app_name = "blog"

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='user_login'),
    url(r'^likepost/$', views.like_post, name='like_post'),
    url(r'^unlikepost/$', views.unlike_post, name='unlike_post'),
    url(r'^postblog/$', views.post_post, name='post_blog'),
    url(r'^editblog/$', views.edit_post, name='edit_blog'),
    url(r'^deleteblog/$', views.delete_post, name='delete_blog'),
    url(r'^shareblog/$', views.share_post, name='share_blog'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns.append(path('', include(router.urls)))
