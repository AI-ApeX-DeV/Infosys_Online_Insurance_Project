from django import forms
from django.contrib.auth.models import User
from .models import AgentAvailability,Appointment,Policy,Feedback
from .models import AgentAvailability,Appointment,Policy
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime
from django.contrib import messages



uri = "mongodb+srv://syed:BMmkQtHjyzPLRyYE@cluster0.yb37t1h.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
client = MongoClient(uri)
db = client['infosys']
agent_availability_collection = db['agent_availability']


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
            'agent': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'agent_phone': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'agent_district': forms.Select(attrs={'class': 'form-control', 'required': True}),'style': 'background-color: transparent;',
            'status': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control', 'required': True}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control', 'required': True}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
            'time_slots': forms.CheckboxSelectMultiple,
        }


def check_time_slot(agent_name, time_slot, date):
    # Query the AgentAvailability model using mongodb
    
    print("inside fucntion")
    # Query the AgentAvailability collection for the specific agent and date
    query = {'agent': agent_name, 'day': date}
    agent_availability = agent_availability_collection.find_one(query)
    print(agent_availability)
    # If agent_availability is None, the agent is not available at all
    if not agent_availability:
        return 1
    
    # Extract the time slots for the agent
    agent_time_slots = agent_availability['free_slots']
    agent_date=agent_availability['day']
    print(agent_date)
    print(agent_time_slots)
    # if time slot in free slot then remove it from free and add it to booked slot 

    if time_slot in agent_time_slots:
        agent_availability_collection.update_one(
            {'agent': agent_name, 'day': date},
            {'$pull': {'free_slots': time_slot}, '$push': {'booked_slots': time_slot}}
        )
        return 2
    else:
        return 3


class SetAppointment(forms.ModelForm):
    class Meta:
        model = Appointment
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
        fields = '__all__'
        
    def clean(self):
        cleaned_data = super().clean()
        select_agent = cleaned_data.get('select_agent')
        time_slots = cleaned_data.get('time_slots')
        date = cleaned_data.get('date')
        print(select_agent)
        print(time_slots)
        print('hellos')
        print(date)
        #print type of date
        print(type(date))
        date_str = date.strftime('%d-%m-%Y')
        print(date_str)
        print(type(date_str))
        # Check if the selected time slot is already booked for the agent
        is_booked = check_time_slot(select_agent.agent, time_slots, date_str)  # Pass the agent's name
    # if is_booked==3:
    #      elif is_booked==1:
    #         raise ValueError(f"Agent {select_agent.agent} is not available on {date_str}.")
    #     else:
    #         pass


class NewPolicy(forms.ModelForm):
    class Meta:
        model = Policy
        fields = '__all__'

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'contact', 'feedback']
        

# from django import forms

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label="Enter your email")

class PasswordResetForm(forms.Form):
    otp = forms.IntegerField(label="Enter OTP")
    new_password = forms.CharField(widget=forms.PasswordInput, label="New Password")
