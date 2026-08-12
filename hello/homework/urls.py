from django.urls import path
from . import views

urlpatterns = [
    path('',views.ViewHomework,name="View HomeWork")
]
