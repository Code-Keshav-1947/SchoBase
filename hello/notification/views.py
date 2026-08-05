from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from notification.models import Notification
# Create your views here.
@login_required
def NotificationListView(request):
    notifications = Notification.objects.filter(user = request.user)
    return render(request, 'notification/notification_list.html', {'notifications': notifications})

@login_required
def mark_notification_as_read(request, pk):
    notification = request.user.notifications.get(pk=pk)
    notification.delete()
    return redirect('notification_list')

@login_required
def mark_all_notifications_as_read(request):
    request.user.notifications.all().delete()
    return redirect('notification_list')