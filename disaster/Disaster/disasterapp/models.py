from django.db import models
from django.utils import timezone

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=100)
    location = models.CharField(max_length=100, default="Global") # To target alerts
    created_at = models.DateTimeField(auto_now_add=True)

class DisasterAlert(models.Model):
    disaster_type = models.CharField(max_length=100) # e.g., Flood, Earthquake
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class PredictionData(models.Model):
    sensor_name = models.CharField(max_length=100)
    value = models.FloatField()
    timestamp = models.DateTimeField(default=timezone.now)