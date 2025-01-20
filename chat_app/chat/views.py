from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from core.models import Messages
from django.db.models import Q
from django.contrib import messages
# Create your views here.

@login_required
def chat_room(request,username=None):
    users = User.objects.exclude(id = request.user.id)
    user_last_message = []
    last_message_timestamp= None
    chats = None
    reciver = None
    if username:
        try:
            reciver = User.objects.get(username=username)
            print(reciver.username)
            chats = Messages.objects.filter(
                (Q(sender=request.user) & Q(receiver=reciver)) |
                (Q(receiver=request.user) & Q(sender=reciver))
            )
            print(chats[1].content)
        except:
            messages.error(request,'Something wents wrong')
    


    for user in users:
        last_message = Messages.objects.filter(
            (Q(sender = request.user)& Q(receiver = user)) |
            (Q(receiver = request.user)& Q(sender = user))
        ).order_by('-timestamp').first()
        if last_message and last_message.timestamp:
            last_message_timestamp = last_message.timestamp
        user_last_message.append({
            'user': user,
            'last_message': last_message,
            'last_message_timestamp':last_message_timestamp,      
        })
        user_last_message.sort(
                key=lambda x: x['last_message_timestamp'],
                reverse=True
            )

    if reciver is None:
        return render(request, 'chat.html', {'users':user_last_message})
    else:
        return render(request, 'chat.html', {'users':user_last_message,'receiver':reciver,'chats':chats})
