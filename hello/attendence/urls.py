from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns =[
  path('take_attendance/',views.take_attendance,name='take_attendance')
  ]