from django.urls import path
from . import views

urlpatterns = [
    path('', views.NotificationListView, name='notification_list'), 
    path('<int:pk>/mark-as-read/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('mark-all-as-read/', views.mark_all_notifications_as_read, name='mark_all_notifications_as_read')
]