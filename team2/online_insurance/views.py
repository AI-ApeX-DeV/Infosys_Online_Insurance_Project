from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import CustomRegistrationForm, CustomLoginForm,AgentRequest
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
import binascii
import folium


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
            return redirect('login')  # Redirect to login page after successful registration
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
                return redirect('display_map')  # Redirect to feedback page after successful login
    else:
        form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})


def display_map(request):
    if request.method == 'POST':
        district = request.POST.get('district').strip()

        # Query the SQLite database for the latitude and longitude of the given district
        # and store the results in a list of dictionaries
        locations = Location.objects.filter(district=district).values('latitude', 'longitude')

        if not locations:
            return render(request, 'map.html', {'district': district, 'error': 'No records found for this district.'})

        # Create a Folium map centered on the first location in the list
        map = folium.Map(location=[locations[0]['latitude'], locations[0]['longitude']], zoom_start=10)

        # Add markers for all the locations in the list
        for location in locations:
            # Create the popup HTML
            popup_html = f"""
            <div style="width: 300px;">
                <h3 style="margin: 0; padding: 10px; background-color: #00704A; color: #FFF; text-align: center; font-size: 20px;">
                    Location
                </h3>
                <div style="padding: 10px;">
                    <p style="margin: 0; margin-bottom: 5px; font-size: 16px;">Latitude: {location['latitude']}</p>
                    <p style="margin: 0; margin-bottom: 5px; font-size: 16px;">Longitude: {location['longitude']}</p>
                </div>
            </div>
            """
            # Add a marker with the popup to the map
            folium.Marker(location=[location['latitude'], location['longitude']], popup=popup_html).add_to(map)

        # Convert the map to HTML
        map_html = map._repr_html_()
        return render(request, 'map.html', {'district': district, 'map_html': map_html})

    # If the request method is not 'POST', return the default map page
    return render(request, 'map.html', {'district': '', 'map_html': '', 'error': ''})

def feedback(request):
    return render (request,'feedback.html')





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
