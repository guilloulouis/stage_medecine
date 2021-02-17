from django.contrib import admin

# Register your models here.
from users.models import Class, ConnectCode, Student

admin.site.register(Class)
admin.site.register(ConnectCode)
admin.site.register(Student)
