from rest_framework import serializers

from django.shortcuts import get_object_or_404

from .models import Card, Product, Order, StatusExeption


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            'name',
            'price',
            'discount_price',]


class OrdersSerializer(serializers.ModelSerializer):

    products = serializers.StringRelatedField(
        many=True)
    order_detail = serializers.HyperlinkedIdentityField(
        view_name='order-detail')

    class Meta:
        model = Order
        fields = [
            'num',
            'date',
            'sell_price',
            'products',
            'order_detail',]


class CreateOrderSerializer(serializers.ModelSerializer):

    products = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Product.objects.all())

    class Meta:
        model = Order
        fields = [
            'products',
        ]

    def create(self, validated_data):
        products = validated_data.pop('products')
        card_number = self.context['view'].kwargs['number']
        products_total_price = 0
        
        try:
            last_order_num = str(int(Order.objects.latest('pk').num)+1)
        except Order.DoesNotExist:
            last_order_num = '0'
            
        for product in products:
            products_total_price += product.discount_price

        card = get_object_or_404(Card, number=card_number)
        order = Order(card=card,
                      **validated_data,
                      sell_price=products_total_price,
                      )

        try:
            order.save(**{'num': last_order_num})
        except StatusExeption:
            raise serializers.ValidationError(StatusExeption.status_message)
        else: 
            card.last_use_date = order.date
            card.total_orders += order.total_price
            card.save()

        for product in products:
            product.order.add(order)

        return order


class BonusCardDetailSerializer(serializers.ModelSerializer):

    orders = OrdersSerializer(many=True)

    class Meta:
        model = Card
        fields = [
            'number',
            'orders',
        ]


class BonusCardListSerializer(serializers.HyperlinkedModelSerializer):

    card_url = serializers.HyperlinkedIdentityField(
        view_name='get-info-about-card', lookup_field='number')

    create_order = serializers.HyperlinkedIdentityField(
        view_name='create-order', lookup_field='number')

    class Meta:
        model = Card
        fields = [
            'number',
            'end_date',
            'last_use_date',
            'state',
            'series',
            'card_url',
            'create_order',
            'discount',
            'total_orders',]
