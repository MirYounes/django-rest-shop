from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework import permissions
from django.contrib.auth import get_user_model
from django.core.cache import cache
from .serializers import (
    UserRegisterSerializer,
    UserRegisterVerfySerializer,
    UserChangePasswordSerializer,
    UserUpdateSerializer,
    UserResetPasswordSerializer,
    UserSetNewPasswordSerializer,
    UserChangeEmailSerializer,
    UserSetNewEmailSerializer
)
from .tasks import send_email_task
from .utils import get_from_redis, delete_from_redis


User = get_user_model()


class UserRegisterApi(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = UserRegisterSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        # Return a 400 response if the data was invalid.
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        if user.is_active:
            content = {'error': 'user already exists'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        send_email_task.delay(
            id=user.id,
            username=user.username,
            email=user.email,
            state='register',
            prefix='verify_email'
        )
        content = {'success': 'your account created , please verify your email'}

        return Response(content, status=status.HTTP_201_CREATED)


class UserRegisterVerifyApi(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = UserRegisterVerfySerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        # Return a 400 response if the data was invalid.
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(email=serializer.validated_data['email'])
        except User.DoesNotExist:
            content = {'error': 'user does not exist'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        token = get_from_redis(user.id, 'register')
        if not token or token != serializer.validated_data['code']:
            content = {'error': 'exired token'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.save()
        delete_from_redis(user.id, 'register')
        content = {'success': 'your email verfied'}

        return Response(content, status=status.HTTP_200_OK)


class UserChangePasswordApi(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserChangePasswordSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(
            data=request.data, instance=request.user)
        # Return a 400 response if the data was invalid.
        serializer.is_valid(raise_exception=True)

        serializer.save()
        content = {'success': 'your password successfuly changed'}

        return Response(content, status=status.HTTP_200_OK)


class UserApi(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserUpdateSerializer

    def get(self, request, format=None):
        serializer = self.serializer_class(instance=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, format=None):
        serializer = self.serializer_class(instance=request.user, data=request.data)
        # Return a 400 response if the data was invalid.
        serializer.is_valid(raise_exception=True)

        serializer.save()
        content = {'success':'user infromation updated'}

        return Response(content, status=status.HTTP_200_OK)


class UserResetPasswordApi(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = UserResetPasswordSerializer

    def post(self, request , format=None):
        serializer = self.serializer_class(data=request.data)   
        # Return a 400 response if the data was invalid.
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(email=serializer.validated_data['email'])
        except User.DoesNotExist:
            content = {'error': 'user does not exist'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        send_email_task.delay(
            id=user.id,
            username=user.username,
            email=user.email,
            state='reset_password',
            prefix='verify_email'
        )
        content = {'success': 'the reset password link has sended'}

        return Response(content, status=status.HTTP_200_OK)


class UserSetNewPasswordApi(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = UserSetNewPasswordSerializer

    def post(self, request , format=None):
        serializer = self.serializer_class(data=request.data)   
        # Return a 400 response if the data was invalid.
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(email=serializer.validated_data['email'])
        except User.DoesNotExist:
            content = {'error': 'user does not exist'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        token = get_from_redis(user.id, 'reset_password')
        if not token or token != serializer.validated_data['token']:
            content = {'error': 'exired token'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(serializer.validated_data['password1'])
        user.save()
        delete_from_redis(user.id, 'reset_password')
        content = {'success':'the password reseted'}

        return Response(content, status=status.HTTP_200_OK)


class UserChangeEmailApi(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserChangeEmailSerializer

    def post(self, request , format=None):
        serializer = self.serializer_class(data=request.data) 
        # Return a 400 response if the data was invalid.
        serializer.is_valid(raise_exception=True)

        user = request.user
        email = serializer.validated_data['email']
        send_email_task.delay(
            id=user.id,
            username=user.username,
            email=email,
            state='change_email',
            prefix='verify_email'
        )
        # delete old email cache
        cache.delete(f'email_{user.id}')
        # set new email cache
        cache.set(f'email_{user.id}', email, 3600)
        content = {'success':'email verfy has sended'}

        return Response(content, status=status.HTTP_200_OK)


class UserSetNewEmailApi(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserSetNewEmailSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data) 
        # Return a 400 response if the data was invalid.
        serializer.is_valid(raise_exception=True)

        user = request.user
        token = get_from_redis(user.id, 'change_email')
        if not token or token != serializer.validated_data['token']:
            content = {'error': 'exired token'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        cache_email = cache.get(f'email_{user.id}')
        if not cache_email or cache_email != email :
            content = {'error': 'exired token'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        user.email = email
        user.save()
        delete_from_redis(user.id, 'change_email')
        cache.delete(f'email_{user.id}')
        content = {'success':'email changed'}

        return Response(content, status=status.HTTP_200_OK)