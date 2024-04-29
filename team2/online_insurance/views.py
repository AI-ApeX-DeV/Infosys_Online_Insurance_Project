from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import CustomRegistrationForm, CustomLoginForm
from django.contrib.auth import authenticate, login
from django import forms

def register(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # Create a new user object and save it
            User.objects.create_user(username=username, email=email, password=password)
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
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('feedback')  # Redirect to home page after successful login
    else:
        form = CustomLoginForm()  # Create an empty form for GET requests
    return render(request, 'login.html', {'form': form})



def feedback(request):
    return render (request,'feedback.html')