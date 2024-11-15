from datetime import timedelta

from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from sqlparse.formatter import validate_options
from django.utils import timezone
from users.models import UserModel, VerificationModel


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(max_length=20, validators=[UniqueValidator(queryset=UserModel.objects.all())])
    password = serializers.CharField(max_length=255, write_only=True)
    class Meta:
        model = UserModel
        fields = ['id','username', 'phone_number','email', 'password', 'confirm_password']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},


        }

    def validate(self, attrs):
            password = attrs.get('password')
            confirm_password = attrs.get('confirm_password')
            if password != confirm_password:
                raise serializers.ValidationError('Passwords must match')
            return attrs

    def validate_phone_number(self, phone_number: str):
        phone_number = phone_number.strip()
        if not phone_number.startswith('+998'):
            raise serializers.ValidationError('Phone number must start with +998')

        if not phone_number[4:].isdigit():
            raise serializers.ValidationError('Phone number must contain only numbers')
        return phone_number

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = UserModel.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def valudate_email(self, email):
        if not email.endswith('@gmail.com') or email.count('@') !=1:
            raise serializers.ValidationError('Email is not correct')
        return email


class VerificationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    code = serializers.CharField(write_only=True)

    class Meta:
        model = VerificationModel
        fields = ['email', 'code']

    def validate(self, attrs):
        try:
            user = UserModel.objects.get(email=attrs['email'])
            user_code = VerificationModel.objects.get(user=user, code=attrs['code'])

        except VerificationModel.DoesNotExist:
            raise serializers.ValidationError('Gmail or code is error')

        current_time = timezone.now()
        if user_code.created_at + timedelta(minutes=2) < current_time:
            user_code.delete()
            raise serializers.ValidationError('Gmail or code is error')
        attrs['user_code'] = user_code
        return attrs


class LoginSerializer(serializers.Serializer):
    email_or_username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)
    errors = 'Email/username or password  is error'

    def validate(self, attrs):
        email_or_username = attrs.get('email_or_username')
        password = attrs.get('password')
        errors = attrs.get('errors')
        try:
            if email_or_username.endswith('@gmail.com'):
                user = UserModel.objects.get(email=email_or_username)
            else:
                user = UserModel.objects.get(username=email_or_username)
        except UserModel.DoesNotExist:
            raise serializers.ValidationError(errors)

        authenticated_user = authenticate(username=user.username, password=password)
        if not authenticated_user:
            raise serializers.ValidationError(errors)
        attrs['user'] = authenticated_user
        return attrs



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        exclude = ['password', 'groups', 'user_permissions', 'is_superuser']
        extra_kwargs = {
            'last_login': {'read_only': True},
            'date_joined': {'read_only': True},
            'is_active': {'read_only': True},
            'is_staff': {'read_only': True},

        }



class ResendCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email')
        try:
            user = UserModel.objects.get(email=email, is_active=True)
        except UserModel.DoesNotExist:
            raise serializers.ValidationError('Email is error')

        user_code = VerificationModel.objects.filter(user__email=email)
        if user_code:
            current_time = timezone.now()
            if user_code.created_at + timedelta(minutes=2) > current_time:
                raise serializers.ValidationError('You have already active code')
        attrs['user'] = user
        return attrs

