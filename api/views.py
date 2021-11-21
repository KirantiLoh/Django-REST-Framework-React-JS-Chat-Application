from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import Room, Message
from .serializers import MessageSerializer, RoomSerializer, MyTokenObtainPairSerializer, UserSerializer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User

# Create your views here.
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def get_routes(request):
    routes = {
        'rooms',
        'rooms/<uuid:uid>',
        'token',
        'token/refresh',
        'register'
    }
    return Response(routes)

@api_view(['POST'])
def register_view(request):
    if request.method == 'POST':
        data = request.data
        try:
            user = User.objects.get(username = data['username'])
            return Response({'message':'Username is taken'}, status = status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            user = User.objects.create(username = data['username'], email=data['email'])
            user.set_password(data['password'])
            user.save()
            serializer = UserSerializer(user, many = False)
            return Response(serializer.data, status = status.HTTP_200_OK)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated,])
def rooms_view(request):
    if request.method == 'GET':
        # room = Room.objects.filter(creator = request.user)
        room = Room.objects.all()
        serializer = RoomSerializer(room, many = True)
        return Response(serializer.data)
    if request.method == 'POST':
        data = request.data
        try:
            room = Room.objects.get(name = data['name'])
            return Response({'message':'A room with that name already exist'}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            user = User.objects.get(username = data['creator'])
            room = Room.objects.create(name = data['name'], creator = user)
            serializer = RoomSerializer(room, many =False)
            return Response(serializer.data)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated,])
def room_view(request, uid):
    try:
        room = Room.objects.get(uid=uid)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = RoomSerializer(room, many = False)
        return Response(serializer.data)
    if request.method == 'POST':
        print(request.data)
        serializer = MessageSerializer(data =request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    if request.method == "PUT":
        name = request.data['name']
        try:
            room = Room.objects.get(name = name)
            return Response({'message':'A room with that name already exist'}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            room.name = name
            room.save()
            serializer = RoomSerializer(room, many = False)
            return Response(serializer.data)
    if request.method == 'DELETE':
        room.delete()
        return Response({'message':'Room Deleted'})

