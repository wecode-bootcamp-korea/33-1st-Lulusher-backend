from tkinter import CASCADE
from django.db import models

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
        
class Product(models.Model):
    sub_category       = models.ForeignKey('SubCategory', on_delete=models.CASCADE)
    name               = models.CharField(max_length=200)
    price              = models.CharField(max_length=30)
    fit_materials_care = models.JSONField(default=dict)
    is_new             = models.BooleanField(default=False)
    is_bestseller      = models.BooleanField(default=False)
    summer_clothes     = models.BooleanField(default=False)

    class Meta:
        db_table = 'products'

class OptionColor(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'options_color'

class OptionSize(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'options_size'

class ProductOption(models.Model): 
    product      = models.ForeignKey('Product', on_delete=models.CASCADE)
    color        = models.ForeignKey('OptionColor', on_delete=models.CASCADE)
    size         = models.ForeignKey('OptionSize', on_delete=models.CASCADE)
    stock        = models.CharField(max_length=30)
    option_price = models.CharField(max_length=30)
    
    class Meta: 
        db_table = 'product_options'
        
class ProductOptionImage(models.Model):
    product_option = models.ForeignKey('ProductOption', on_delete=models.CASCADE)
    image_url      = models.URLField(max_length=1000)
    
    class Meta:
        db_table = 'product_options_images'

class Activity(models.Model): 
    activity_name = models.CharField(max_length=30)
    products      = models.ManyToManyField('Product', through="ProductActivity")
    
    class Meta:
        db_table = 'activities'

class ProductActivity(models.Model):
    activity = models.ForeignKey('Activity', on_delete=models.CASCADE)
    product  = models.ForeignKey('Product', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'product_activities'