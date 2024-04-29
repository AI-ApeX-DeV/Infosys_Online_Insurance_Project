from django.db import models

# Create your models here.
class UserInfo(models.Model):
    
    name=models.CharField(max_length=200)
    age=models.IntegerField()
    mail=models.EmailField()
    password=models.CharField(max_length=200)
    


