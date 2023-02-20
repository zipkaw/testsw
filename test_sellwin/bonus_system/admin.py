from django.contrib import admin
from .models import Card, Order, Product 

# Register your models here.

admin.site.register(Order)
admin.site.register(Product)

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    pass

