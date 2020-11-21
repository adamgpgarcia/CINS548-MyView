from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class User(models.Model):
    username=models.CharField(max_length=10, primary_key=True)
    password=models.CharField(max_length=20)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
class ViewUser(models.Model):
    #id = models.AutoField(primary_key=True)
    username=models.CharField(max_length=30)
    MacAdd=models.CharField(max_length=20)
    url=models.URLField(max_length=200)
    connect=models.BooleanField(default='False')
