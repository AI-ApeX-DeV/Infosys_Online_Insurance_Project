"""
URL configuration for team2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from online_insurance import views
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls,name="admin"),
    path('map/',views.map,name="map"),
    path('',views.register,name="Register"),
    path('login/password_reset_request', views.password_reset_request_view, name='password_reset_request'),
    path('password_reset_verify_otp/', views.password_reset_verify_otp, name='password_reset_verify_otp'),
    path('login/',views.user_login,name="login"),
    path('feedback/', views.feedback, name='feedback'),
    path('feedback/success/', views.feedback_success, name='feedback_success'),
    path("login/home/",views.home,name="home"),
    #path('agent/', views.set_availability, name="agent" ),
    #path('members/details/<int:id>', views.details, name='details'),
    #path('members/', views.members, name='members'),
    path('agent-update/',views.agentupdate,name="agent-update"),
    path('500/',views.agent,name="500"),
    path('logout/',RedirectView.as_view(url='/admin/logout/')),
    path("appointment/",views.appointment,name="appointment"),
    path("policy/",views.PolicyUpdate,name="policy"),
    path("policy/details",views.details,name="details"),
    path('login/home/login/',views.user_login)
    
    ]
    

