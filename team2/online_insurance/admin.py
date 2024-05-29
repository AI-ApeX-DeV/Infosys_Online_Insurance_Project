from django.contrib import admin
<<<<<<< HEAD
from .models import AgentAvailability,Appointment,Policy
# Register your models here
=======
from .models import AgentAvailability,Appointment,Policy,UserProfile
# Register your models here.
from .forms import PasswordResetRequestForm,PasswordResetForm
>>>>>>> 1f937d421d20b6d2761b6549d813601cbde6afa2

admin.site.register(AgentAvailability)
admin.site.register(Appointment)
from django.contrib import admin
from .models import Policy

class PolicyAdmin(admin.ModelAdmin):
    list_display = ('policy_name', 'price')#'formatted_str'

    # def formatted_str(self, obj):
    #     return str(obj)
    # formatted_str.short_description = 'Policy Details'

admin.site.register(Policy, PolicyAdmin)
admin.site.register(UserProfile)

