from django.urls import path, include
from . import views

urlpatterns =[
  path('take/', views.take_attendance, name='take_attendance'),
  ]