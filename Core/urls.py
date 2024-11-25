
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/',include('users.urls')),
    path('follower/',include('follower.urls')),
    path('tweet/', include('comment.urls')),
]
