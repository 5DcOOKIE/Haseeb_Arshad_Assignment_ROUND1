from django.contrib.auth.models import User
from knox.models import AuthToken
from rest_framework import viewsets, generics
from rest_framework.response import Response

from users.serializers.user import UserSerializer, RegisterSerializer, LoginSerializer


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

    @classmethod
    def get_extra_actions(cls):
        return []


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        user_obj = User.objects.get(username=user['email'])
        token = AuthToken.objects.create(user_obj)[1]

        return Response({
            "user_id": UserSerializer(user_obj).data['id'],  # Get serialized User data
            "token": token
        })
