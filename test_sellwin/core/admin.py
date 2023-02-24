from django.contrib import admin
from .models import Card, Order, Product


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = [
        'number',
        'series',
        'state',
        'discount',
        'last_use_date',
        'total_orders',
    ]
    list_filter = (
        'series',
        'state',
        'last_use_date'
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'num',
        'date',
        'sell_price',
    ]
    list_filter = (
        'date',
    )
    fields = [
        'date',
        'sell_price',
    ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'price',
        'discount_price',
    ]
    list_filter = (
        'price',
        'discount_price',
    )
