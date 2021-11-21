from django.core.checks import messages
from rest_framework import serializers
from .models import Room, Message
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['name'] = user.username

        return token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(
        slug_field = 'username',
        queryset = User.objects.all()
    )
    class Meta:
        model = Message
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True)
    creator = serializers.SlugRelatedField(
        slug_field = 'username',
        queryset = User.objects.all()
    )
    class Meta:
        model = Room
        fields = ['uid', 'name', 'creator', 'date_created', 'messages']