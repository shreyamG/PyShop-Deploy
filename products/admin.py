from django.contrib import admin
from .models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')


class OfferAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount')


admin.site.register(Product, ProductAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
# admin.site.register(models.ShippingAddress)
# admin.site.register(models.ProductDetails)
