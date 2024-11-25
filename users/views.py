import threading


from users.serializers import VerificationSerializer, UserProfileSerializer, UsersSerializer

from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status
from users.models import UserModel
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import RegistrationSerializer,LoginSerializer, ResendCodeSerializer
from users.signals import sent_verification_email


class RegisterView(generics.CreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.is_active = True
        user.save()
        return user


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]
    serializer_class = VerificationSerializer

    def post(self, request):
        serializer = VerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_code = serializer.validated_data['user_code']
        user = user_code.user

        user.is_active = True
        user.save()
        user_code.delete()
        response = {
            "success": True,
            "message": "Verification code has been sent.",
        }
        return Response(response, status=status.HTTP_200_OK)


class LoginView(APIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh = RefreshToken.for_user(serializer.validated_data['user'])
        response = {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
        }
        return Response(response, status=status.HTTP_200_OK)


class ResendEmailView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ResendCodeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        email_thread = threading.Thread(target=sent_verification_email, args=(email,))
        email_thread.start()
        response = {
            "success": True,
            "message": "Verification new code has been sent for your email",
        }
        return Response(response, status=status.HTTP_200_OK)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get(self, request):
        user = self.request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    def delete(self, request):
        user = self.request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SearchView(APIView):
    queryset = UserModel.objects.all()
    permission_classes = [IsAdminUser]
    def get(self, request):

        users= UserModel.objects.all()

        search = request.query_params.get('search')
        page = int(request.query_params.get('page'))
        page_size = int(request.query_params.get('page_size', 2))
        if search:
            users = users.filter(username__icontains=search)
        if page:
            page -=1
            users = users[page * page_size: page * page_size + page_size]
        serializer = UsersSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


