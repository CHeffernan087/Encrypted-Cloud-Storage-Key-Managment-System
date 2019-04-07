from django.db import models
from django import forms

# Create your models here.
class User(models.Model):
    userName = models.CharField(max_length=200)
    pubKey =  models.CharField(max_length=1024)

class File(models.Model):
    title = forms.CharField(max_length=50)
    file = forms.FileField()