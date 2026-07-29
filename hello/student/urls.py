from django.urls import include, path
from . import views

app_name = 'student'

urlpatterns = [
    path('', views.index, name='student'),
    path('create_student/', views.create_student, name='create_student'),
    path('list_students/', views.student_list, name='student_list'),
    path('update_student/<int:pk>/', views.update_student, name='update_student'),
    path('delete_student/<int:pk>/', views.delete_student, name='delete_student'),
]