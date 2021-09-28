from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from .models import Profile


User = get_user_model()


class UserRegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    is_provider = serializers.BooleanField(default=False)
    password1 = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError("password must match")
        return attrs

    def create(self, validated_data):
        user = None
        try:
            user = User.objects.get(
                email=validated_data['email'])
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password1'],
                is_provider=validated_data['is_provider'],
                is_active=False
            )
        return user


class UserRegisterVerfySerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True)


class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    password1 = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    def validate_old_password(self, value):
        if not self.instance.check_password(value):
            raise serializers.ValidationError(
                'old password must equal to corrent password')
        return value

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError("password must match")
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password1'])
        instance.save()
        return instance


class ProfileSerializer(serializers.ModelSerializer):
    class Meta :
        model = Profile
        fields = ('bio', 'avatar', 'age')


class UserUpdateSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name','profile')
        read_only_fileds = [
            'email'
        ]
        extra_kwargs = {
            'username': {'required': False},
            }
    
    def update(self, instance, validated_data):  
        if validated_data.get('pforile'):
            profile_serializer = self.fields['profile']
            profile_instance = instance.profile
            profile_data = validated_data.pop('profile')
            profile_serializer.update(profile_instance, profile_data)
        return super().update(instance, validated_data)


class UserResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def vlaidate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'the user with that email does no exist')

        return value


class UserSetNewPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    email = serializers.EmailField()
    password1 = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError("password must match")
        return attrs


class UserChangeEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])


class UserSetNewEmailSerializer(serializers.Serializer):
    token = serializers.CharField()
    email = serializers.EmailField()
