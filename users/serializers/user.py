from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models.user import User
from users.utils import validate_email


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'is_staff', 'username', 'gender', 'age')


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(validated_data['email'], validated_data['password'])


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            # Check if user sent email
            if validate_email(email):
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
            msg = ('Must include "email" and "password"',)
            raise ValidationError(msg)

        attrs['user'] = user
        return attrs
