from rest_framework import serializers

from django.shortcuts import get_object_or_404

from core.models import Card, Product, Order


FILE_NAME = '_db_data.json'
FILE_DIR = './test_data_json/'


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model=Card
        fields='__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields='__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'