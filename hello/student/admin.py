from django.contrib import admin
from .models import Student

# Register your models here.
admin.site.register(Student)

admin.site.site_header = "My SchoBase Admin"  # Top navbar heading
admin.site.site_title = "SchoBase Admin Portal"  # Browser tab title
admin.site.index_title = "Welcome to the Portal"  # Main dashboard subtitle
