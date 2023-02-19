
from django_filters import rest_framework as filters

from .models import Order, Card


class OrderDateFilter(filters.FilterSet):

    order__date = filters.DateTimeFilter(method='filter_order_date')

    class Meta:
        model = Order
        fields = {
            'date': ['gt']
        }


class BonusCardFilter(filters.FilterSet):

    date_gt = filters.DateFilter(
        method='filter_order_date_gt', field_name='orders')

    class Meta:
        model = Card
        fields = ['orders']

    def filter_order_date_gt(self, queryset, name, value):
        card_obj = Card.objects.get(
            number=self.request.query_params.get('number'))
        card_obj.orders.set(Order.objects.filter(sell_price__gt=20))
        return card_obj


class OrderFilter(filters.FilterSet):
    date_range = filters.DateFromToRangeFilter(
        field_name='date', label='Date range')

    class Meta:
        model = Order
        fields = ['date_range']
