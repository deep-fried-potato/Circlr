from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# class UserProfile_Model(models.Model):
#    username=models.OneToOneField(User,on_delete=models.CASCADE);
#    city = models.CharField(max_length=100,null=True);
#    phone = models.IntegerField(default=10);
#
#
#    def __str__(self):
#            return str(self.username)


class Interest_Model(models.Model):
    username=models.ForeignKey(User,on_delete=models.CASCADE);
    interest = models.CharField(max_length=100,default='');

    def __str__(self):
            return str(self.username)

class Friends_Status(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name="sender");
    receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name="receiver")
    status = models.BooleanField()

    def __str__(self):
        return str(self.receiver)
