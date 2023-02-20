
from django_filters import rest_framework as filters

from .models import Order, Card


class BonusCardFilter(filters.FilterSet):

    date_gt = filters.DateFilter(
        method='filter_order_date', field_name='date_greater')
    date_lt = filters.DateFilter(
        method='filter_order_date', field_name='date_less')

    @staticmethod
    def lookup_expr(expr: str, name: str, value) -> dict:
        """Lookup expresion constructor, return  dictionary with expression and value"""
        return {'__'.join([name, expr]): value}

    def filter_order_date(self, queryset, name, value):
        card_obj = queryset
        card_obj.orders.set(Order.objects.filter(
            **self.lookup_expr(name.replace('date_', ''), 'date', value)))
        return card_obj