from django.db import models
from core      import TimeStampModel

from users.models    import User
from products.models import Product 

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