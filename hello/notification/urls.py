from django.urls import path
from . import views

urlpatterns = [
    path('', views.notification_list, name='notification_list'),
    path('mrk_as_read/<int:message_id>', views.mrk_as_read, name='mrk_as_read'),
    path('delete_notification/',views.delete_notification,name='delete_notification')
]