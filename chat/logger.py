import os
from chat.models import Message
from django.contrib.auth.models import User
from django.db.models import Q
from .validator import *

def unique(sequence):
    seen = set()
    return [x for x in sequence if not (x[0].username in seen or seen.add(x[0].username))]

def log_message(sender,roomname,message):
    Message.objects.create(sender=User.objects.get(username=sender),roomname=roomname,message=message,receiver=User.objects.get(username=receiver_gen(sender,roomname)))

def load_log(roomname):
    return Message.objects.filter(roomname=roomname)

def get_recents(username):
    messagelist=Message.objects.filter(Q(sender__username=username)|Q(receiver__username=username)).order_by('-timestamp')
    recentlist = []
    for message in messagelist:
        if roomvalidate(username,message.roomname):
            recentlist.append((receiver_gen(username,message.roomname),message.sender,message.message,message.timestamp))
    return unique(recentlist)

def print_path():
    print(os.path.abspath(__file__))
