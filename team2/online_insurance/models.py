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
    agent=models.CharField(max_length=100,default='Default Agent')
    agent_phone=models.IntegerField()
    status=models.CharField(max_length=20,choices=[('available','Available'),('unavailable','Unavailable')])
    start_time=models.DateTimeField()
    end_time=models.DateTimeField()
    lattitude=models.IntegerField()
    longitude=models.IntegerField()

    def __str__(self):
        return f"{self.agent} {self.agent_phone} {self. status} {self.start_time} {self.end_time} {self.lattitude} {self.longitude} "
    


