from django.db import models

# Create your models here.
class Site (models.Model):
    id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length= 100)
    Address = models.CharField(max_length = 250)
    City = models.CharField(max_length = 100)
    Country = models.CharField(max_length = 100)
