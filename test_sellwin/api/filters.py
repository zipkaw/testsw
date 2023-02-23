from django_filters import rest_framework as filters


class OrdersFilter(filters.FilterSet):

    date_gt = filters.DateFilter(
        method='filter_order_date', 
        field_name='date_gt'
    )
    date_lt = filters.DateFilter(
        method='filter_order_date', 
        field_name='date_lt'
    )

    @staticmethod
    def lookup_expr(expr: str, name: str, value) -> dict:
        """
        Lookup expresion constructor, return  dictionary 
        with expression and value
        """
        return {'__'.join([name, expr]): value}

    def filter_order_date(self, queryset, name, value):
        return queryset.filter(**self.lookup_expr(
            name.replace('date_', ''),
            'date',
            value
        ))
