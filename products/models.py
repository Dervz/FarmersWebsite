from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class Categories(models.Model):
    title = models.CharField(max_length = 250)
    
    def __str__(self):
        return self.title
                             
class Product(models.Model):
    title        = models.CharField(max_length = 250)
    price        = models.DecimalField(max_digits=4, decimal_places=2)
    quantity     = models.IntegerField()
    description  = models.TextField()
    image        = models.ImageField(upload_to = 'media/')
    category     = models.ForeignKey(Categories, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
    
class Orders(models.Model):
    
    name          = models.CharField(max_length=128)
    user          = models.ForeignKey(User, on_delete=models.CASCADE)
    orderTotal    = models.DecimalField(max_digits=4, decimal_places=2)
    orderProducts = models.ManyToManyField(Product, through='OrderDetails')
    
    def __str__(self):
        return self.name
    
class OrderDetails(models.Model):
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    order    = models.ForeignKey(Orders, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total    = models.DecimalField(max_digits=4, decimal_places=2)

