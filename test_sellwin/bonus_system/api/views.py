from rest_framework import generics
from rest_framework.reverse import reverse as rest_reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.db.models import Prefetch

from bonus_system.models import Card, Order, Product
from .filters import OrdersFilter
from .serializers import (BonusCardListSerializer,
                          BonusCardDetailSerializer,
                          OrdersSerializer,
                          ProductSerializer,
                          CreateOrderSerializer)


@api_view(['GET'])
def api_root(request, format=None):
    response_kwargs = {'request': request, 'format': format}
    return Response({
        'cards': rest_reverse('card-list', **response_kwargs),
        'orders': rest_reverse('order-list', **response_kwargs),
        'products': rest_reverse('product-list', **response_kwargs),
    })


class CardList(generics.ListAPIView):
    queryset = Card.objects.all()
    serializer_class = BonusCardListSerializer
    lookup_field = 'number'


class OrderList(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrdersSerializer


class OrderDetail(generics.RetrieveAPIView):
    serializer_class = OrdersSerializer

    def get_object(self):
        return Order.objects.get(id=self.kwargs['pk'])


class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class InfoAboutCard(generics.RetrieveAPIView):
    serializer_class = BonusCardDetailSerializer
    lookup_field = 'number'
    filterset_class = OrdersFilter

    def get_object(self):
        card_obj = Card.objects.filter(number=self.kwargs['number'])
        orders = self.filter_queryset(card_obj.first().orders)
        card_obj = card_obj.prefetch_related(Prefetch(queryset=orders,
                                                      lookup='orders'))
        return card_obj.first()


class CreateOrders(generics.CreateAPIView):
    serializer_class = CreateOrderSerializer
    lookup_field = 'number'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['number'] = self.kwargs['number']
        return context

    def get_object(self):
        obj = Order.objects.filter(card=self.kwargs['number'])
        self.check_object_permissions(self.request, obj)
        return obj