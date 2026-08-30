"""
URL configuration for hello project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView    

urlpatterns = [
    path("admin/", admin.site.urls),
    # API POST
    path("api/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include("dashboard.urls"), name="dashboard"),
    path("acc/", include("accounts.urls"), name="accounts"),
    path("student/", include("student.urls"), name="student"),
    path("teacher/", include("teacher.urls"), name="teacher"),
    path("notification/", include("notification.urls"), name="notification"),
    path("attendance/", include("attendence.urls"), name="attendance"),
    path("homework/", include("homework.urls"), name="homework"),
    path("api/", include("api.urls"), name="api"),
    # path('school/', include('school.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
]
handler404 = "django.views.defaults.page_not_found"
handler403 = 'django.views.defaults.permission_denied'

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
