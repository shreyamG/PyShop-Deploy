from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from django.db.models import prefetch_related_objects



class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    stock = models.IntegerField()
    image_url = models.CharField(max_length=2083)
    # image = models.ImageField(upload_to='product_images', blank=True, null=True, default=None) using pillow, "Choose file to upload"

    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='customer', null=True, blank=True)
    name = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)
    
    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null = True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=255)
    
    def __str__(self):
        return str(self.id)
    
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total() for item in orderitems])
        return total
    
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null = True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null = True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
# ShippingAddress Part2 12:06

class Offer(models.Model):
    code = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    discount = models.FloatField()