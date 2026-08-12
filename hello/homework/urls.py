from django.urls import path
from . import views

urlpatterns = [
    path('',views.ViewHomework,name="view homework"),
    path('send/',views.sendHomework,name="send homework"),
]
