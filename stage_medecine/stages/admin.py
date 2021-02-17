from django.contrib import admin

# Register your models here.
from stages.models import StageDone, Stage, Category, Period

admin.site.register(StageDone)
admin.site.register(Stage)
admin.site.register(Category)
admin.site.register(Period)
