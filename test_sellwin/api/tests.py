from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.reverse import reverse

import json

from .models import Card, Order, Product
from .serializers import BonusCardDetailSerializer


class CardDetailTest(APITestCase):
    def setUp(self) -> None:
        self.card = Card.objects.create(**{
            "series": "DF",
            "number": "0000000000000012",
            "release_date": '2023-02-23T15:30:17Z',
            "end_date": '2023-08-23T15:30:17Z',
            "last_use_date": '2023-04-23T15:30:17Z',
            "total_orders": 0,
            "state": "NA",
            "discount": 3,
            "deleted": True})
        self.url = reverse('get-info-about-card',
                           kwargs={'number': self.card.number})
        self.serializer = BonusCardDetailSerializer(instance=self.card)
        self.client = APIClient()

    def test_retrieve_my_model(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.serializer.data)


class CreateOrderTest(APITestCase):

    def setUp(self):
        self.card = Card.objects.create(**{
            "series": "DF",
            "number": "000000000000000",
            "release_date": '2023-02-23T15:30:17Z',
            "end_date": '2023-08-23T15:30:17Z',
            "last_use_date": '2023-04-23T15:30:17Z',
            "total_orders": 0,
            "state": "NA",
            "discount": 3,
            "deleted": True})
        self.product1 = Product.objects.create(
            name='Product 1',
            price=10,
            discount_price=8)
        self.product2 = Product.objects.create(
            name='Product 2',
            price=20,
            discount_price=16)
        self.valid_payload = {
            'products': self.product1.id,
        }
        self.invalid_payload = {
            'products': [],
        }

    def test_create_valid_order(self):
        url = reverse(
            'create-order',
            kwargs={'number': self.card.number})
        response = self.client.post(
            url,
            data=json.dumps(self.valid_payload),
            format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(self.card.total_orders, 28)

    def test_create_invalid_order(self):
        url = reverse(
            'create-order',
            kwargs={'number': self.card.number})
        response = self.client.post(
            url,
            data=json.dumps(self.invalid_payload),
            format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(self.card.total_orders, 0)
