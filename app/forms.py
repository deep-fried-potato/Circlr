from django import forms
from app.models import Interest_Model,Friends_Status
from django.contrib.auth.models import User



class registration_form(forms.ModelForm):


    class Meta:
        model=User
        fields=['username','first_name','last_name','email',]


class Forms_city(forms.ModelForm):

    class Meta:
        model=Interest_Model
        exclude = ['username',]

class Searchu(forms.Form):
    search_namebyuser = forms.CharField(max_length=100, required=True)
class Searchi(forms.Form):
    search_namebyinterest = forms.CharField(max_length=100, required=True)


class SendRequest(forms.ModelForm):

    class Meta:
        model=Friends_Status
        fields = ['receiver',]




class ConfirmRequest(forms.ModelForm):
    #Username2=forms.CharField(label="friend requests:", widget=forms.Select(choices=requests))
    class Meta:
        model=Friends_Status
        fields = ['sender',]
