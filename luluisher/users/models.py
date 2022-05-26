from django.db       import models
from products.models import Product


# Create your models here.

class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class User(TimeStampModel):
    name            = models.CharField(max_length=100)
    email           = models.CharField(max_length=100, unique=True)
    password        = models.CharField(max_length=100)
    mobile_number   = models.CharField(max_length=100)
    address         = models.CharField(max_length=100)
    email_subscribe = models.BooleanField(default=False)

    class Meta: 
        db_table = "users"

class Cart(TimeStampModel):
    user      = models.ForeignKey(User, on_delete=models.CASCADE)
    product   = models.ForeignKey(Product, on_delete=models.CASCADE)
    image_url = models.URLField(max_length=1000)
    quantity  = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'product'], name = 
            'name of constraint')
        ]
        db_table = 'carts'