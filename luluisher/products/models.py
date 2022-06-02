from django.db    import models

from core import TimeStampModel

class Menu(models.Model):
    name = models.CharField(max_length=30)
    
    class Meta:
        db_table = 'menus'
        
class MainCategory(models.Model):
    menu = models.ForeignKey('Menu', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    
    class Meta:
        db_table = 'main_categories'
        
class SubCategory(models.Model):
    main_category = models.ForeignKey('MainCategory', on_delete=models.CASCADE)
    name          = models.CharField(max_length=30)
    
    class Meta:
        db_table = 'sub_categories'
        
class Product(TimeStampModel):
    sub_category       = models.ForeignKey('SubCategory', on_delete=models.CASCADE)
    name               = models.CharField(max_length=200)
    price              = models.IntegerField(default=0)
    fit_materials_care = models.JSONField(default=dict)
    is_new             = models.BooleanField(default=False)
    is_bestseller      = models.BooleanField(default=False)
    summer_clothes     = models.BooleanField(default=False)

    class Meta:
        db_table = 'products'

class OptionColor(TimeStampModel):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'option_colors'

class OptionSize(TimeStampModel):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'option_sizes'

class ProductOption(TimeStampModel): 
    product      = models.ForeignKey('Product', on_delete=models.CASCADE)
    color        = models.ForeignKey('OptionColor', on_delete=models.CASCADE)
    size         = models.ForeignKey('OptionSize', on_delete=models.CASCADE)
    stock        = models.CharField(max_length=30)
    option_price = models.CharField(max_length=30)
    
    class Meta: 
        db_table = 'product_options'
        
class ProductOptionImage(TimeStampModel):
    product_option = models.ForeignKey('ProductOption', on_delete=models.CASCADE)
    image_url      = models.URLField(max_length=1000)
    
    class Meta:
        db_table = 'product_options_images'

class Activity(TimeStampModel): 
    activity_name = models.CharField(max_length=30)
    products      = models.ManyToManyField('Product', through="ProductActivity")
    
    class Meta:
        db_table = 'activities'

class ProductActivity(TimeStampModel):
    activity = models.ForeignKey('Activity', on_delete=models.CASCADE)
    product  = models.ForeignKey('Product', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'product_activities'

class Review(TimeStampModel):
    content = models.CharField(max_length=500)
    rating  = models.IntegerField(default=0)
    user    = models.ForeignKey('users.User', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        db_table = 'reviews'

