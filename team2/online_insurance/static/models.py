from django.db import models
from django.contrib.auth.models import User
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import timedelta
from datetime import date


uri = "mongodb+srv://syed:BMmkQtHjyzPLRyYE@cluster0.yb37t1h.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
client = MongoClient(uri)
db = client['infosys']
agent_availability_collection = db['agent_availability']


TIME_SLOT_CHOICES = [
    ('1-2', '1-2'),
    ('2-3', '2-3'),
    ('3-4', '3-4'),
    ('4-5', '4-5'),
    ('5-6', '5-6'),
    ('6-7', '6-7'),
    ('7-8', '7-8'),
    ('8-9', '8-9'),
    ('9-10', '9-10'),
    ('10-11', '10-11'),
    ('11-12', '11-12'),
    ('12-13', '12-13'),
    ('13-14', '13-14'),
    ('14-15', '14-15'),
    ('15-16', '15-16'),
    ('16-17', '16-17'),
    ('17-18', '17-18'),
    ('18-19', '18-19'),
    ('19-20', '19-20'),
    ('20-21', '20-21'),
    ('21-22', '21-22'),
    ('22-23', '22-23'),
    ('23-24', '23-24'),
]

# Create your models here.
class UserInfo(models.Model):
    
    name=models.CharField(max_length=200)
    age=models.IntegerField()
    mail=models.EmailField()
    password=models.CharField(max_length=200)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp_secret = models.CharField(max_length=32, blank=True, null=True)

class AgentAvailability(models.Model):
    #agent=models.ForeignKey(User,on_delete=models.CASCADE)
    agent=models.CharField(max_length=100,default='')
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
    ],verbose_name='District')
    status=models.CharField(max_length=20,choices=[('available','Available'),('unavailable','Unavailable')],verbose_name='Status')
    start_time=models.DateTimeField()
    end_time=models.DateTimeField()
    lattitude=models.FloatField()
    longitude=models.FloatField()
    time_slots = models.CharField(max_length=300, verbose_name='Time Slots',default="")

    def save(self, *args, **kwargs):
        # Convert time_slots string to a list
        if isinstance(self.time_slots, str):
            self.time_slots = self.time_slots.split(',')
        
        # Save to MongoDB
        delta = self.end_time.date() - self.start_time.date()
        for i in range(delta.days + 1):
            date = self.start_time.date() + timedelta(days=i)
            date_str = date.strftime('%d-%m-%Y')

            # Save free and booked slots for each date
            data = {
                'day': date_str,
                'agent': self.agent,
                'time_slots': self.time_slots,
                'free_slots': self.time_slots,
                'booked_slots': [],
            }
            agent_availability_collection.insert_one(data)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.agent}"
    



class Appointment(models.Model):
    Name=models.ForeignKey(User,on_delete=models.CASCADE,null=False)
    select_agent=models.ForeignKey(AgentAvailability,on_delete=models.CASCADE,null=False)
    date = models.DateField(default=date.today)
    time_slots = models.CharField(max_length=300,choices=TIME_SLOT_CHOICES, verbose_name='Time Slots', default="")
    reason=models.TextField(null=False)

    def __str__(self):
        return f"{self.Name}"


    

class Policy(models.Model):
    policy_name=models.CharField(max_length=200)
    PolicyType=models.CharField(max_length=200,null=True)
    Policy_Number=models.IntegerField(null=True)
    price=models.IntegerField(null=True)
    RenewalDate=models.CharField(max_length=200,null=True)
    Contact_Info=models.CharField(max_length=100,null=True)


    def __str__(self):
        return f"name - {self.policy_name}    price - {self.price}"

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    contact = models.CharField(max_length=15)
    feedback = models.TextField()

    def __str__(self):
        return self.name
   