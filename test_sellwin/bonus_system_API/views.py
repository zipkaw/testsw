from rest_framework.views import APIView
from rest_framework.response import Response

from ..bonus_system.models import Card, Order, Product
from .serializers import OrdersSerializer, ProductSerializer, BonusCardSerializer

class InfoAboutCard(APIView): 

    def get(self, request): 
        pass 
        return Response(...)
