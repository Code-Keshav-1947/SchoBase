from django.urls import path
# imports the viewsets
from .views import StudentViewSet, TeacherViewSet, SchoolViewSet, SectionViewSet, NotificationViewSet, AttendanceViewSet, ClassViewSet

urlpatterns = [
    path('students/', StudentViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('teachers/', TeacherViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('schools/',SchoolViewSet.as_view({'get':'list','post':'create'})),
    path('sections/',SectionViewSet.as_view({'get':'list','post':'create'})),
    path('classes/',ClassViewSet.as_view({'get':'list','post':'create'})),
    path('notifications/',NotificationViewSet.as_view({'get':'list','post':'create'})),
    path('attendances/',AttendanceViewSet.as_view({'get':'list','post':'create'})),
]
