from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey(User,on_delete = models.CASCADE,related_name="tosender")
    receiver = models.ForeignKey(User,on_delete = models.CASCADE,related_name="toreceiver",default = 1)
    roomname = models.CharField(max_length = 100)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)
