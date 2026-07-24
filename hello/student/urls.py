from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='student'),
    path('create/', views.create, name='student-create'),
    path('list/', views.student_list, name='student-list'),
    path('update/<int:pk>/', views.update, name='student-update'),
    path('delete/<int:pk>/', views.delete, name='student-delete'),
]