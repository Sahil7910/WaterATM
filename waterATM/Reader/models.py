from django.db import models
from django.utils import timezone
from Site.models import Site


# Create your models here.
class Configuration(models.Model):
    id = models.AutoField(primary_key=True)
    SERVER_IP = models.CharField(max_length= 100)
    DURATION_1LTR = models.IntegerField()
    DURATION_2LTR = models.IntegerField()
    DURATION_3LTR = models.IntegerField()
    DURATION_5LTR = models.IntegerField()


class Reader(models.Model):
    id = models.AutoField(primary_key=True)
    position = models.IntegerField()
    mac = models.CharField(max_length=100, unique=True)
    install_date = models.DateTimeField(default=timezone.now)
    last_seen_timestamp = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10)
    config = models.ForeignKey(Configuration, on_delete=models.CASCADE)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    def __str__(self):
        return f"Reader {self.mac} - Status: {self.status}"


