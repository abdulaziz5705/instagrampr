from django.urls import path
from rest_framework.routers import DefaultRouter
from comment import views
router = DefaultRouter()
router.register(r'', views.TweetViewSet)
router.register(r'comment', views.TweetCommentViewSet)


urlpatterns = [
    path('child/', views.TweetChildListApiView.as_view())

] + router.urls