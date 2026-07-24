from django.urls import path, include
from . import views 

urlpatterns = [
    path('', views.teacher_profile, name='teacher_profile'), 
]