from django.urls import path
from .views import StudentViewSet, TeacherViewSet

urlpatterns = [
    path('students/', StudentViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('teachers/', TeacherViewSet.as_view({'get': 'list', 'post': 'create'})),
]
