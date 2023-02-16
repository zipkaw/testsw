from rest_framework import serializers
from .models import Card, Product, Order

# product -> order -> card 

class ProductSerializer(serializers.ModelSerializer):

    class Meta: 
        model = Product
        fields = ['name']


class OrdersSerializer(serializers.ModelSerializer):
    
    product = ProductSerializer(read_only=True)
    
    class Meta: 
        model = Order
        fields = ['num', 'date', 'sell_price']


class BonusCardSerializer(serializers.ModelSerializer):

    orders = OrdersSerializer(many=True)

    class Meta:
        model = Card
        fields = ['number', 'orders']
    