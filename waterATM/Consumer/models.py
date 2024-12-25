from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class Consumer(AbstractUser):
    id = models.AutoField(primary_key=True)  # Auto-incrementing ID
    name = models.CharField(max_length=255)  # Name of the consumer
    gender = models.CharField(max_length=10)
    age = models.PositiveIntegerField()  # Age, must be a positive number

    def __str__(self):
        return self.name

class Membership(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    number = models.CharField(max_length=20, unique=True)  # Membership number, must be unique
    status = models.CharField(max_length=10)
    consumer_id = models.ForeignKey('Consumer',on_delete=models.CASCADE,related_name='memberships')

    def __str__(self):
        return f"Membership {self.number} ({self.status})"
