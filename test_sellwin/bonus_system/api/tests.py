from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.reverse import reverse

from .models import Card, Order, Product
from .serializers import BonusCardDetailSerializer


class CardDetailTest(APITestCase):
    def setUp(self) -> None:
        self.url = reverse('get-info-about-card')
        self.card = Card.objects.create(
            number='000000000000',
            series='SF',
        )
        self.serializer = BonusCardDetailSerializer(instance=self.card)
        self.client = APIClient()

    def test_retrieve_my_model(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.serializer.data)


class CreateOrderTest(APITestCase):
    
    def setUp(self):
        self.card = Card.objects.create(number='0000000000000000')
        self.product1 = Product.objects.create(name='Test product 1', price=10, discount_price=8)
        self.product2 = Product.objects.create(name='Test product 2', price=20, discount_price=16)
        self.data = {
            'products': [self.product1.id, self.product2.id],
        }

    def test_create_order(self):
        url = reverse('create-orders', kwargs={'number': self.card.number})
        response = self.client.post(url, data=self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(self.card.total_orders, 24)
        self.assertEqual(self.card.last_use_date, Order.objects.first().date)

    def test_create_order_with_invalid_products(self):
        invalid_product_id = 999
        self.data['products'].append(invalid_product_id)
        url = reverse('create-orders', kwargs={'number': self.card.number})
        response = self.client.post(url, data=self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)
