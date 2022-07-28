from django.contrib.auth import get_user_model
from knox.models import AuthToken
from rest_framework import viewsets, generics
from rest_framework.response import Response

from users.serializers.user import UserSerializer, RegisterSerializer, LoginSerializer

User = get_user_model()


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print("post", serializer)
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
        user = UserSerializer(user_obj).data
        return Response({
            "user_id": user['id'],
            "token": token
        })
