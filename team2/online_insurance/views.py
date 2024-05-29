from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django import forms
from .models import AgentAvailability,Policy
from django.template import loader
from .forms import CustomRegistrationForm, CustomLoginForm,AgentRequest,SetAppointment,NewPolicy
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
import binascii
import folium
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from django.views.generic import TemplateView
from django.contrib import messages

uri = "mongodb+srv://syed:BMmkQtHjyzPLRyYE@cluster0.yb37t1h.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
client = MongoClient(uri)
db = client['infosys']
agent_availability_collection = db['agent_availability']


class ErrorPageView(TemplateView):
    template_name = 'error_page.html'

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

            string = username + password
            short_hash = generate_short_hash(string)

            # Create a new user object and save it
            User.objects.create_user(username=username, email=email, password=short_hash)
            return redirect("login")  # Redirect to login page after successful registration
    else:
        form = CustomRegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            string = username + password
            short_hash = generate_short_hash(string)
            user = authenticate(request, username=username, password=short_hash)
            if user is not None:
                login(request, user)
                return redirect("home/")  # Redirect to feedback page after successful login
    else:
        form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})



def map(request):
    if request.method == 'POST':
        district = request.POST.get('district').strip()

        # Query AgentAvailability objects for the given district
        agent_locations = AgentAvailability.objects.filter(agent_district=district)

        if not agent_locations:
            return render(request, 'map.html', {'district': district, 'error': 'No records found for this district.'})

        # Create a Folium map centered on the first agent location
        map = folium.Map(location=[agent_locations[0].lattitude, agent_locations[0].longitude], zoom_start=10)

        # Add markers for all the agent locations
        for agent_location in agent_locations:
            # Create the popup HTML
            popup_html = f"""
            <div style="width: 300px;">
                <h3 style="margin: 0; padding: 10px; background-color: #00704A; color: #FFF; text-align: center; font-size: 20px;">
                    Agent: {agent_location.agent}
                </h3>
                <div style="padding: 10px;">
                    <p style="margin: 0; margin-bottom: 5px; font-size: 16px;">Phone: {agent_location.agent_phone}</p>
                    <p style="margin: 0; margin-bottom: 5px; font-size: 16px;">Status: {agent_location.status}</p>
                    <p style="margin: 0; margin-bottom: 5px; font-size: 16px;">Start Time: {agent_location.start_time}</p>
                    <p style="margin: 0; margin-bottom: 5px; font-size: 16px;">End Time: {agent_location.end_time}</p>
                  
                </div>
            </div>
            """
            # Add a marker with the popup to the map
            folium.Marker(location=[agent_location.lattitude, agent_location.longitude], popup=popup_html).add_to(map)

        # Convert the map to HTML
        map_html = map._repr_html_()
        return render(request, 'map.html', {'district': district, 'map_html': map_html})

    # If the request method is not 'POST', return the default map page
    return render(request, 'map.html', {'district': '', 'map_html': '', 'error': ''})

def home(request):
    return render (request,'aboutus.html')

def feedback(request):
    return render (request,'feedback.html')

def agent_availability_view(request):
    agent_availabilities = AgentAvailability.objects.all()



def agent(request):
    agents = AgentAvailability.objects.all()
    context={'agents':agents}
    return render(request,'500.html',context)

def agentupdate(request):
    form = AgentRequest()
    if request.method == 'POST':
        form = AgentRequest(request.POST)
        if form.is_valid:
            form.save()
            return redirect('500')
    context={'form':form}
    return render(request,'agent.html',context)


def appointment(request):
    form = SetAppointment()
    try:
        if request.method == 'POST':
            form = SetAppointment(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/admin/')
        context = {'form': form}
        return render(request, 'appointment.html', context)
    except Exception as e:
        messages.error(request, "The time slot is already booked for the agent or not available")
        return render(request, 'appointment.html', {'form': form})

def PolicyUpdate(request):
    form=NewPolicy()
    if request.method == 'POST':
        form = NewPolicy(request.POST)
        if form.is_valid:
            form.save()
            return redirect("details")
    context = {'form': form }
    return render(request,'policy.html',context)

def details(request):
    policy=Policy.objects.all()
    context={"policy":policy}
    return render(request,"details.html",context)


