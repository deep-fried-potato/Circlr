from django.shortcuts import render,redirect
from .forms import Forms_city,registration_form,Searchu,Searchi
from .models import Interest_Model,Friends_Status
from django.contrib.auth.models import User
from collections import Counter
from django.http import HttpResponse
import json
from django.contrib.auth.decorators import login_required
# Create your views here.

def View_city(request):
    form = Forms_city()
    registration = registration_form()
    if request.method == "POST":
        form = Forms_city(request.POST)
        registration = registration_form(request.POST)
        if form.is_valid() and registration.is_valid():
            registrationdata=registration.save()
            formdata=form.save(commit=False)
            formdata.username=registrationdata
            print(registrationdata)
            interest_var=form.cleaned_data['interest']
            interest_var=interest_var.lower().replace(" ","")
            interest_var = interest_var.lower().replace(","," ").split(" ")
            interest_var = list(filter(None, interest_var))
            print(registrationdata.username)
            for var in interest_var:
                a=User.objects.get(username=registrationdata.username);
                Interest_Model.objects.create(username=a ,interest=var);
    return render(request, 'app/profile.html',{'form':form,'registration':registration})




@login_required(login_url='/admin')
def sendr(request):
    if request.method == 'POST':
        req=request.POST['req']
        receiver=User.objects.get(username=req)
        if not Friends_Status.objects.filter(sender=request.user,receiver=receiver,status=False):
            Friends_Status.objects.create(sender=request.user,receiver=receiver,status=False)
        response_data={}

        try:
            response_data['success']='Friend Request Sent'
        except:
            response_data['success']='Error Sending Request'
    return HttpResponse(json.dumps(response_data), content_type="application/json")




@login_required(login_url='/admin')
def acceptr(request):
    if request.method == 'POST':
        accept=request.POST['receiver']
        print('------->>>>>>>'+str(accept))
        sender=User.objects.get(username=accept)
        Friends_Status.objects.filter(sender=sender,receiver=request.user,status=False).update(status=True)

        response_data={}

        try:
            response_data['success']='Friend Request Accepted'
        except:
            response_data['success']='error accepting request'
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url='/admin')
def decliner(request):
    if request.method == 'POST':
        decline=request.POST['receiver']
        option=request.POST['option']
        sender=User.objects.get(username=decline)
        Friends_Status.objects.filter(sender=sender,receiver=request.user).delete()

        response_data={}

        if option == '0':
            try:
                response_data['success']='Friend Request Declined'
            except:
                response_data['success']='error Declining request'
        else :
            try:
                response_data['success']='UnFriended'
            except:
                response_data['success']='error unfriending'
    return HttpResponse(json.dumps(response_data), content_type="application/json")






@login_required(login_url='/admin')
def matching(request):
        form=Searchu(request.POST)
        form1=Searchi(request.POST)

        allusers=Interest_Model.objects.all()
        getfriends1=Friends_Status.objects.filter(sender=request.user, status=True)
        getfriends2=Friends_Status.objects.filter(receiver=request.user, status=True)
        pendingfriends=Friends_Status.objects.filter(receiver=request.user, status=False)
        pendingfriends1=Friends_Status.objects.filter(sender=request.user)
        pendingfriends2=Friends_Status.objects.filter(receiver=request.user)

        filteringbutton=[]
        pendingfrnd=[]
        friends=[]
        for frnd in getfriends1:
            friends.append(frnd.receiver.username)
        for frnd in getfriends2:
            friends.append(frnd.sender.username)
        for frnds in pendingfriends:
            pendingfrnd.append(frnds.sender.username)
        for frnds in pendingfriends2:
            filteringbutton.append(frnds.sender.username)
        for frnd in pendingfriends1:
            filteringbutton.append(frnd.receiver.username)
        suggestionlist=[]
        pendingfrnd=list(set(pendingfrnd))
        print("-->pending frnd"+str(pendingfrnd))
        print("--->flteringbutton"+str(filteringbutton))

        #for suggestion finding current user city and interests

        curruserinterest=[]
        curruser=User.objects.get(username=request.user.username)
        print(curruser)
        cr1_interest=Interest_Model.objects.filter(username=curruser)
        print('--------')
        for i in cr1_interest:
                curruserinterest.append(i.interest);
        print(curruserinterest)

        suggestionlist=[]

        for intrst in curruserinterest:
            suggtemp = Interest_Model.objects.filter(interest=intrst)
            for i in suggtemp:
                if str(i.username) != request.user.username:
                    suggestionlist.append(i.username)
        print('suggestionlist')
        print(suggestionlist)
        suggestionlist.sort(key=Counter(suggestionlist).get, reverse=True)
        suggestionlist = [ e
                    for i, e in enumerate(suggestionlist)
                    if suggestionlist.index(e) == i
                ]

        suggestionlist= [x for x in suggestionlist if x.username not in friends]
        print("suggestionlist:->"+str(suggestionlist))


        if form.is_valid():
            text=form.cleaned_data['search_namebyuser']
            list2=[]
            if User.objects.filter(username__icontains=text).count()>0:
                srchuser=User.objects.filter(username__icontains=text)
                for i in srchuser:
                    list2.append(i.username)
            # userlist=Interest_Model.objects.all()
            # print(userlist)
            # list2=[]
            # for user in userlist:
            #     if str(user.username) == text:
            #         list2.append(user.username)
            return render(request, 'app/friendsugg.html', {'userlist':list2,'form':form,'form1':form1,'text':text,'suggestionlist':suggestionlist, 'friends':friends,'pendingfrnds':pendingfrnd, 'filteringbutton':filteringbutton})

        elif form1.is_valid():
            text1=form1.cleaned_data['search_namebyinterest']
            text1 = text1.lower().replace(","," ").split(" ")
            text1 = list(filter(None, text1))
            list1=[]
            for intrst in text1:
                temp = Interest_Model.objects.filter(interest=intrst)
                for i in temp:
                    if str(i.username) != request.user.username:
                        list1.append(i.username)
            print(list1)
            list1.sort(key=Counter(list1).get, reverse=True)
            list1 = [ e
                        for i, e in enumerate(list1)
                        if list1.index(e) == i
                    ]


            # for user in allusers:
            #     if str(user.username)!=request.user.username:
            #         interestlist=str(user.interest)
            #         #citylist=str(user.city)
            #         interestlist = interestlist.lower().replace(","," ").split(" ")
            #         interestlist = list(filter(None, interestlist))
            #         if set(text1)==set(interestlist):
            #             #print(interestlist)
            #             list1.append(user.username)
            return render(request, 'app/friendsugg.html', {'interestlist':list1,'form':form,'form1':form1,'text1':text1,'curruserinterest':curruserinterest,'suggestionlist':suggestionlist,'friends':friends,'pendingfrnds':pendingfrnd, 'filteringbutton':filteringbutton})
        args = {'form':form,'form1':form1,'suggestionlist':suggestionlist,'friends':friends,'pendingfrnds':pendingfrnd,'filteringbutton':filteringbutton}
        return render(request, 'app/friendsugg.html', args)











        # for user in allusers:
        #     if str(user.username)==request.user.username:
        #         currusercity=user.city
        #         currusercity=currusercity.lower()
        #         curruserinterest=str(user.interest)
        #         curruserinterest = curruserinterest.lower().replace(","," ").split(" ")
        #         curruserinterest = list(filter(None, curruserinterest))
        #
        # #otheruserlist = Interest_Model.objects.filter(interest__in=curruserinterest)
        # #print(otheruserlist)
        # for user in allusers:
        #     if str(user.username)!=request.user.username:
        #         otheruserinterest=str(user.interest)
        #         otheruserinterest = otheruserinterest.lower().replace(","," ").split(" ")
        #         otheruserinterest = list(filter(None, otheruserinterest))
        #         for item in curruserinterest:
        #             if item in otheruserinterest:
        #                 suggestionlist.append(user.username)
        #     #suggestionlist.append(user.username)
        #
        # for user in allusers:
        #     if str(user.username)!=request.user.username:
        #         if str(user.city.lower()) == currusercity:
        #             suggestionlist.append(user.username)
        #
        # # interestlist=Interest_Model.objects.filter(interest__in=text1)
        # suggestionlist.sort(key=Counter(suggestionlist).get, reverse=True)
        # suggestionlist = [ e
        #                 for i, e in enumerate(suggestionlist)
        #                   if suggestionlist.index(e) == i
        #                 ]
        #
        #
        # if form.is_valid():
        #     text=form.cleaned_data['search_namebyuser']
        #     userlist=Interest_Model.objects.all()
        #     print(userlist)
        #     list2=[]
        #     for user in userlist:
        #         if str(user.username) == text:
        #             list2.append(user.username)
        #     return render(request, 'app/friendsugg.html', {'userlist':list2,'form':form,'form1':form1,'text':text,'suggestionlist':suggestionlist, 'friends':friends,'pendingfrnds':pendingfrnd})
        #
        # elif form1.is_valid():
        #     text1=form1.cleaned_data['search_namebyinterest']
        #     text1 = text1.lower().replace(","," ").split(" ")
        #     text1 = list(filter(None, text1))
        #     list1=[]
        #
        #     for user in allusers:
        #         if str(user.username)!=request.user.username:
        #             interestlist=str(user.interest)
        #             #citylist=str(user.city)
        #             interestlist = interestlist.lower().replace(","," ").split(" ")
        #             interestlist = list(filter(None, interestlist))
        #             if set(text1)==set(interestlist):
        #                 #print(interestlist)
        #                 list1.append(user.username)
        #     return render(request, 'app/friendsugg.html', {'interestlist':list1,'form':form,'form1':form1,'text1':text1,'currusercity':currusercity,'curruserinterest':curruserinterest,'suggestionlist':suggestionlist,'friends':friends,'pendingfrnds':pendingfrnd})
        # args = {'form':form,'form1':form1,'suggestionlist':suggestionlist,'friends':friends,'pendingfrnds':pendingfrnd}
        # return render(request, 'app/friendsugg.html', args)
