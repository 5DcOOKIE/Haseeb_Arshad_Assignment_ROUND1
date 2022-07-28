from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from rest_framework.exceptions import ValidationError


# User Serializer
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'is_staff', 'username')


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user


def validateEmail(email):
    try:
        User.objects.get(email=email)
        return False
    except User.DoesNotExist:
        return True


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            # Check if user sent email
            if validateEmail(email):
                user_request = get_object_or_404(
                    User,
                    email=email,
                )

                email = user_request.username

            user = authenticate(username=email, password=password)

            if user:
                if not user.is_active:
                    msg = ('User account is disabled.',)
                    raise ValidationError(msg)
            else:
                msg = ('Unable to log in with provided credentials.',)
                raise ValidationError(msg)
        else:
            msg = ('Must include "email or username" and "password"',)
            raise ValidationError(msg)

        attrs['user'] = user
        return attrs
