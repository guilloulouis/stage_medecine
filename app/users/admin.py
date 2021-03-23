from django.contrib import admin

# Register your models here.
from users.models import Class, Student

admin.site.register(Class)
admin.site.register(Student)
