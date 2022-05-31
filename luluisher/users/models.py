from django.db       import models
from products.models import Product

from core           import TimeStampModel

# Create your models here.

class User(TimeStampModel):
    name            = models.CharField(max_length=100)
    email           = models.CharField(max_length=100, unique=True)
    password        = models.CharField(max_length=100)
    mobile_number   = models.CharField(max_length=100)
    address         = models.CharField(max_length=100)
    email_subscribe = models.BooleanField(default=False)

    class Meta: 
        db_table = "users"
