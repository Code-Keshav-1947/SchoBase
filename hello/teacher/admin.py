from django.contrib import admin
from .models import Teacher
# Register your models here.
admin.site.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'class_teacher_of', 'school')
    
    def display_class_teacher_of(self, obj):
        return ", ".join([str(class_obj) for class_obj in obj.class_teacher_of.all()])
    
    display_class_teacher_of.short_description = 'Class Teacher Of'