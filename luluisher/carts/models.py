from django.db import models
from core      import TimeStampModel

from users.models    import User
from products.models import ProductOption

class Cart(TimeStampModel):
    user           = models.ForeignKey(User, on_delete=models.CASCADE)
    product_option = models.ForeignKey(ProductOption, on_delete=models.CASCADE)
    quantity       = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'product_option'], name = 
            'name of constraint')
        ]
        db_table = 'carts' 
