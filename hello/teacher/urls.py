from django.urls import path
from . import views

urlpatterns = [
    path("", views.teacher_profile, name="teacher_profile"),
    path("list_teachers/", views.list_teachers, name="list_teachers"),
]
