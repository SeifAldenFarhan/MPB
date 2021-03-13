from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path

from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include('blog.urls', namespace='app')),
    url(r'^logout/$', views.user_logout, name='logout'),
    # path('api-auth/', include('rest_framework.urls'))
]
