from django.db import models

from Consumer.models import Membership
from Reader.models import Reader


# Create your models here.

class Quota (models.Model):
    id = models.AutoField(primary_key= True)
    Gender = models.CharField(max_length = 10)
    DAILY_QUOTA = models.CharField(max_length=50)
    ACTIVE_DATE = models.DateTimeField(auto_now_add=True)
    Status = models.CharField(max_length=10)

class Transaction(models.Model):
    id = models.AutoField(primary_key= True)
    Txn_DateTime=models.DateTimeField(auto_now_add=True)
    CONSUMED_QTY = models.CharField(max_length = 50)
    BALANCE_QTY = models.CharField(max_length = 50)
    MEMBERSHIP_ID=models.ForeignKey(Membership,on_delete=models.SET_NULL, null=True,blank=True )
    READER_ID = models.ForeignKey(Reader, on_delete= models.SET_NULL, null= True, blank = True)

