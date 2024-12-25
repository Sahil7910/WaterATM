from django.db import models

from Site.models import Site


# Create your models here.
class Configuration(models.Model):
    id = models.AutoField(primary_key=True)
    SERVER_IP = models.CharField(max_length= 100)
    DURATION_1LTR = models.IntegerField(max_length = 20)
    DURATION_2LTR = models.IntegerField(max_length = 20)
    DURATION_3LTR = models.IntegerField(max_length = 20)
    DURATION_5LTR = models.IntegerField(max_length = 20)


class Reader(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incrementing ID
    position = models.IntegerField()  # Position of the reader
    mac = models.CharField(max_length=100, unique=True)  # Unique MAC address
    install_date = models.DateTimeField(auto_now_add=True)  # Installation date
    last_seen_timestamp = models.DateTimeField(null=True, blank=True)  # Last seen timestamp
    status = models.CharField(max_length=10)  # Status with predefined choices
    config = models.ForeignKey(Configuration, on_delete=models.SET_NULL, null=True,blank=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE )  # Foreign key to Site model

    def __str__(self):
        return f"Reader {self.mac} - Status: {self.status}"


