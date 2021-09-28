from os import name
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    UserRegisterApi,
    UserRegisterVerifyApi,
    UserChangePasswordApi,
    UserResetPasswordApi,
    UserSetNewPasswordApi,
    UserChangeEmailApi,
    UserSetNewEmailApi,
    UserApi
)

app_name = 'accounts'
urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegisterApi.as_view(), name='register_api'),
    path('register/verify/', UserRegisterVerifyApi.as_view(),
         name='register_verify_api'),
    path('password/change/', UserChangePasswordApi.as_view(),
         name='user_change_password_api'),
    path('password/reset/', UserResetPasswordApi.as_view(), name='reset_password'),
    path('password/reset/confirm/', UserSetNewPasswordApi.as_view(),
         name='reset_password_confirm'),
    path('email/change/',UserChangeEmailApi.as_view(), name='change_email'),
    path('email/change/confirm/', UserSetNewEmailApi.as_view(), name='change_email_confirm'),
    path('profile/', UserApi.as_view(), name='user_detail')
]
