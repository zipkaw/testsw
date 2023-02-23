from django.test import TestCase, Client
from django.urls import reverse

from ..core.models import Card, Order
from .forms import BonusCardStateForm


class CardListViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.url = reverse('all-cards')

    def test_get_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bonus_system/card_list.html')


class CardDetailViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.card = Card.objects.create(
            number='0000000000000001', 
            series='SA', 
            state='AC',)
        self.url = reverse('card', args=[str(self.card.pk)])

    def test_get_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bonus_system/card_detail.html')
        self.assertContains(response, self.card.number)

    def test_post_valid_form(self):
        data = {'state': 'AC',
                'change status': 'Submit'}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('card', args=[self.card.pk]))
        self.card.refresh_from_db()
        self.assertEqual(self.card.state, 'AC')

    def test_post_invalid_form(self):
        data = {'state': '', 'change+status': 'Submit'}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bonus_system/card_detail.html')
        self.assertFormError(
            response,
            'form',
            'state',
            'This field is required.')

    def test_context_data(self):
        order = Order.objects.create(kwargs={'card': self.card, 'num': '0'})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['orders'], [repr(order)])
        self.assertIsInstance(response.context['form'], BonusCardStateForm)


class CardGenerateForm(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.url = reverse('generate')

    def test_get_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bonus_system/card_create.html')

    def test_post_valid_form(self):
        data = {'series': 'DF',
                'generate': 'Create cards',
                'release_date': '2023-02-21+18:23:18',
                'end_date': '2023-08-21+18:23:18',
                'card_count': '1'}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('all-cards'))
        card = Card.objects.get(release_date='2023-02-21+18:23:18')
        self.assertEqual(card.state, 'NA')

    def test_post_invalid_form(self):
        data = {'series': '',
                'generate': 'Create cards',
                'release_date': '2023-02-21+18:23:18',
                'end_date': '2023-08-21+18:23:18',
                'card_count': '1'}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bonus_system/card_create.html')
        self.assertFormError(
            response,
            'form',
            'series',
            'This field is required.')


class TrashListViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.url = reverse('trash')

    def test_get_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bonus_system/trash.html')
