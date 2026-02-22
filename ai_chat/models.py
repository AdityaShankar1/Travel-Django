from django.db import models

# Create your models here.
# bookings/models.py
class Place(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='places/') # Allows uploading photos