from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
from .models import Notification

# Create your views here.
@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user)
    return render(request, 'notification/notification_list.html',{'notifications':notifications})

@login_required
def mrk_as_read(request,message_id):
    notification = Notification.objects.filter(id = message_id).delete()
    return redirect(notification_list)

@login_required
def delete_notification(request):
    Notification.objects.filter(user = request.user).delete()
    return redirect(notification_list)