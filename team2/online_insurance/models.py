from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserInfo(models.Model):
    
    name=models.CharField(max_length=200)
    age=models.IntegerField()
    mail=models.EmailField()
    password=models.CharField(max_length=200)

class AgentAvailability(models.Model):
    #agent=models.ForeignKey(User,on_delete=models.CASCADE)
    agent=models.CharField(max_length=100)
    agent_phone=models.IntegerField()
    agent_district = models.CharField(max_length=100, choices=[
        ('Ahmadnagar', 'Ahmadnagar'),
        ('Akola', 'Akola'),
        ('Amravati', 'Amravati'),
        ('Aurangabad', 'Aurangabad'),
        ('Bhandara', 'Bhandara'),
        ('Buldhana', 'Buldhana'),
        ('Chandrapur', 'Chandrapur'),
        ('Dhule', 'Dhule'),
        ('Gadchiroli', 'Gadchiroli'),
        ('Gondia', 'Gondia'),
        ('Hingoli', 'Hingoli'),
        ('Jalgaon', 'Jalgaon'),
        ('Jalna', 'Jalna'),
        ('Kolhapur', 'Kolhapur'),
        ('Latur', 'Latur'),
        ('MumbaiCity', 'Mumbai City'),
        ('MumbaiSuburban', 'Mumbai Suburban'),
        ('Nagpur', 'Nagpur'),
        ('Nanded', 'Nanded'),
        ('Nandurbar', 'Nandurbar'),
        ('Nashik', 'Nashik'),
        ('Osmanabad', 'Osmanabad'),
        ('Palghar', 'Palghar'),
        ('Parbhani', 'Parbhani'),
        ('Pune', 'Pune'),
        ('Raigad', 'Raigad'),
        ('Ratnagiri', 'Ratnagiri'),
        ('Sangli', 'Sangli'),
        ('Satara', 'Satara'),
        ('Sindhudurg', 'Sindhudurg'),
        ('Solapur', 'Solapur'),
        ('Thane', 'Thane'),
        ('Wardha', 'Wardha'),
        ('Washim', 'Washim'),
        ('Yavatmal', 'Yavatmal'),
    ])
    status=models.CharField(max_length=20,choices=[('available','Available'),('unavailable','Unavailable')])
    start_time=models.DateTimeField()
    end_time=models.DateTimeField()
    lattitude=models.FloatField()
    longitude=models.FloatField()

    def __str__(self):
        return f"{self.agent}"
    

class Appointment(models.Model):
    Name=models.ForeignKey(User,on_delete=models.CASCADE,null=False)
    select_agent=models.ForeignKey(AgentAvailability,on_delete=models.CASCADE,null=False)
    time_from = models.TimeField()
    time_to = models.TimeField()
    reason=models.TextField(null=False)
   
    def __str__(self):
        return f"{self.Name}"

    

class Policy(models.Model):
    policy_name=models.CharField(max_length=200)
    price=models.IntegerField()

    def __str__(self):
        return f"name - {self.policy_name}    price - {self.price}"
