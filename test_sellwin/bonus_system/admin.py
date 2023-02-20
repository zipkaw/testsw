from django.contrib import admin
from .models import Card, Order, Product

# Register your models here.

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass
