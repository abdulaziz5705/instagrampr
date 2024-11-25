from django.urls import path

from follower import views

urlpatterns = [
    path('following/', views.FollowingView.as_view(), name='following'),

]