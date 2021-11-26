from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import Profile, Room, Message, Profile
from .serializers import MessageSerializer, ProfileSerializer, RoomSerializer, MyTokenObtainPairSerializer, UserSerializer
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
            profile = Profile.objects.create(user = user)
            profile.save()
            serializer = UserSerializer(user, many = False)
            return Response(serializer.data, status = status.HTTP_200_OK)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated,])
def rooms_view(request):
    if request.method == 'GET':
        rooms = request.user.rooms.all()
        serializer = RoomSerializer(rooms, many = True)
        return Response(serializer.data)
    if request.method == 'POST':
        data = request.data
        try:
            room = Room.objects.get(name = data['name'])
            return Response({'message':'A room with that name already exist'}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            user = User.objects.get(username = data['creator'])
            room = Room.objects.create(name = data['name'], creator = user)
            user.rooms.add(room)
            serializer = RoomSerializer(room, many =False)
            return Response(serializer.data)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated,])
def room_view(request, uid):
    try:
        room = Room.objects.get(uid=uid)
        cur_user = request.user
        if not (room.creator != cur_user or room.members.filter(username = cur_user).exists()):
            return Response({'message':'You are not a member of this room'}, status=status.HTTP_400_BAD_REQUEST)
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


@api_view(['POST', 'PUT'])
@permission_classes([IsAuthenticated,])
def profile_view(request):
    data = request.data
    try:
        user = User.objects.get(username = data['user'])
    except ObjectDoesNotExist:
        return Response({'message':'User was not found'})
    if request.method == 'POST':
        try:
            room = Room.objects.get(uid = data['uid'])
            creator = User.objects.get(username = data['creator'])
            print(creator == room.creator)
            if creator == room.creator:
                user.rooms.add(room)
                user.save()
                print(user.rooms.all())
                return Response({'message':'User has been added to room!'})
            return Response({'message':'Error'})
        except ObjectDoesNotExist:
            return Response({'message':"Room doesn't exist"})
    if request.method == 'PUT':
        data = request.data
        try:
            room = Room.objects.get(uid = data['uid'])
            creator = User.objects.get(username = data['creator'])
            print(creator == room.creator)
            if creator == room.creator:
                user.rooms.remove(room)
                user.save()
                print(user.rooms.all())
                return Response({'message':'User has been removed from the room!'})
            return Response({'message':'Error'})
        except ObjectDoesNotExist:
            return Response({'message':"Room doesn't exist"})

