from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField()
    password = models.CharField(max_length=200)
    username = models.CharField(max_length=200,unique=True)
    image = models.ImageField()

class FriendRequest(models.Model):
    request_user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='friend_request_user')
    requested_by_user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True, related_name='friend_request_requested_user')
    status = models.CharField(max_length=200,default='Pending')

class Message(models.Model):
    reciever = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='message_reciever')
    sender = models.ForeignKey(User,on_delete=models.SET_NULL,null=True, related_name='message_sender')
    message = models.TextField(null=True)