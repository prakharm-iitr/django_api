from abc import ABC

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserLoginHistory


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password')
        # extra_kwargs = {
        #     'password': {'write_only': True}
        # }

    def save(self):
        user = User(
            username=self.validated_data["username"]
        )
        user.set_password(self.validated_data['password'])
        user.save()
        return


class LoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    username = serializers.CharField(max_length=128)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'password')


class LoginHistorySerializer(serializers.ModelSerializer):
    """Serializer for saving login attempt"""
    # password = serializers.CharField(write_only=True)

    class Meta:
        model = UserLoginHistory
        fields = ('user_id', 'ip_addr')
