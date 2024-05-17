from django.contrib import admin
from .models import AgentAvailability,Appointment
# Register your models here.

admin.site.register(AgentAvailability)
admin.site.register(Appointment)