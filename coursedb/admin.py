from django.contrib import admin

# Register your models here.

from .models import School, Department, Course

admin.site.register(School)
admin.site.register(Department)
admin.site.register(Course)
