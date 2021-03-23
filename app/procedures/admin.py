from django.contrib import admin

# Register your models here.
from procedures.models import Procedure, StageWish, Simulation, TemporaryStageDone

admin.site.register(Procedure)
admin.site.register(StageWish)
admin.site.register(Simulation)
admin.site.register(TemporaryStageDone)
