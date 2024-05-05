from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import CustomRegistrationForm, CustomLoginForm, AgentRequest
from django.contrib.auth import authenticate, login
from django import forms
from .models import AgentAvailability
import binascii
from django.http import HttpResponse
from django.template import loader
from .models import AgentAvailability


def generate_short_hash(string):
    # Calculate the CRC32 hash
    crc32_hash = binascii.crc32(string.encode('utf-8'))

    # Convert the hash to a positive integer
    crc32_hash = crc32_hash & 0xffffffff

    # Convert the hash to a 5-character hexadecimal string
    short_hash = format(crc32_hash, 'x')[:5]

    return short_hash

def register(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            string=username+password
            short_hash = generate_short_hash(string)

            # Create a new user object and save it
            User.objects.create_user(username=username, email=email, password=short_hash)
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = CustomRegistrationForm()
    return render(request, 'register.html', {'form': form})



def user_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)  # Pass POST data to the form
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            string=username+password
            short_hash = generate_short_hash(string)
            user = authenticate(request, username=username, password=short_hash)
            if user is not None:
                login(request, user)
                return redirect('feedback')  # Redirect to home page after successful login
    else:
        form = CustomLoginForm()  # Create an empty form for GET requests
    return render(request, 'login.html', {'form': form})

def set_availability(request):
    if request.method == 'POST':
        form = AgentRequest(request.POST)
        if form.is_valid():
            availability = form.save(commit=False)
            availability.agent = request.user  # Assuming agents are authenticated users
            availability.save()
            return redirect('feedback')  # Redirect to a success page or home page
    else:
        form = AgentRequest()
    return render(request, 'set_availability.html', {'form': form})


def feedback(request):
    return render (request,'feedback.html')

def agent_availability_view(request):
    agent_availabilities = AgentAvailability.objects.all()

    return render(request, 'all_agents.html', {'agent_availabilities': agent_availabilities}) 

def members(request):
  mymembers = AgentAvailability.objects.all()
  template = loader.get_template('all_agents.html')
  context = {
    'mymembers': mymembers,
  }
  return HttpResponse(template.render(context, request))

  
def details(request, id):
  mymember = AgentAvailability.objects.get(id=id)
  template = loader.get_template('details.html')
  context = {
    'mymember': mymember,
  }
  return HttpResponse(template.render(context, request))