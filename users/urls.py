from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users import views


urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('verify/email/', views.VerifyEmailView.as_view(), name='verifyemail'),
    path('verify/code/', views.ResendEmailView.as_view(), name='resendcode'),
    path('me/', views.ProfileView.as_view(), name='profile'),
    path('search/', views.SearchView.as_view(), name='search'),


    path('api/token/',TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/',TokenRefreshView.as_view(), name='token_refresh'),
]