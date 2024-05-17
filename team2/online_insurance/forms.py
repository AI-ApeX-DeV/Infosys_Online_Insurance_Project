from django import forms
from django.contrib.auth.models import User
from .models import AgentAvailability,Appointment


class CustomRegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150)
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already registered.")
        return email


class CustomLoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class AgentRequest(forms.ModelForm):
    class Meta:
        model= AgentAvailability
        fields= '__all__'
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class SetAppointment(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'
        widgets = {
                'time_from': forms.TimeInput(attrs={'type': 'time'}),
                'time_to': forms.TimeInput(attrs={'type': 'time'}),
            }
            
