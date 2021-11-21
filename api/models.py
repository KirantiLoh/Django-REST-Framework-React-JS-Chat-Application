from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Room(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} : {self.content}"

"""
class FriendList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField(User, related_name="friends", blank=True)

    def add_friend(self, account):
        if not account  in self.friends.all():
            self.friends.add(account)
            self.save()
    
    def remove_friend(self, account):
        self.friends.remove(account)
    
    def unfriend(self, removee):
        remomer_friend_list = self

        remomer_friend_list.remove_friend(removee)

        friend_list = FriendList.objects.get(user=removee)
        friend_list.remove_friend(self.user)
    
    def is_mutual_friend(self, friend):
        if friend in self.friends.all():
            return True
        return False

    def __str__(self):
        return f"{self.user}'s Friend List"
"""
