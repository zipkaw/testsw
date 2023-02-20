
# from django.utils.decorators import method_decorator
# from django.views.decorators.cache import cache_page

from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from rest_framework import viewsets
from rest_framework.renderers import StaticHTMLRenderer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.reverse import reverse_lazy
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import FormMixin, ModelFormMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.detail import BaseDetailView
from django.db.models import Q
from django.utils import timezone

from .forms import BonusCardStateForm, BonusCardGenerateForm
from .models import Card, Order, Product
from .mixins import UpdateFieldMixin
from .serializers import BonusCardListSerializer, BonusCardDetailSerializer, OrdersSerializer, ProductSerializer, CreateOrderSerializer
from .filters import OrdersFilter


class BonusCardDetailView(generic.DetailView, FormMixin):
    model = Card
    form_class = BonusCardStateForm

    def get_success_url(self) -> str:
        self.object = self.get_object()
        return reverse('card', args=[self.get_object().pk])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(card=context['card'])
        context['form'] = self.get_form()
        return context

    def get_initial(self):
        current_state = self.get_object().state
        return {'state': current_state}

    def form_valid(self, form):
        self.object = self.get_object()
        cleaned_data = form.cleaned_data
        # add update
        self.object.state = cleaned_data['state']
        self.object.save()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if 'change status' in request.POST:
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)


class BonusCardListView(generic.ListView):
    model = Card
    paginate_by = 5

    def get_queryset(self):
        query_to_update = Card.objects.filter(end_date__lt=timezone.now())
        if query_to_update:
            query_to_update.update(state='OD')
        return super().get_queryset()


class BonusCardGenerateView(generic.TemplateView, FormMixin):
    template_name = 'bonus_system/card_create.html'
    form_class = BonusCardGenerateForm
    card_numbers = None

    def get_success_url(self) -> str:
        return reverse('all-cards')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if 'generate' in request.POST:
            if form.is_valid():
                cleaned_data = form.clean()
                self.card_numbers = form.get_generated_cards()
                for card_num in self.card_numbers:
                    card = Card(number=card_num, release_date=cleaned_data['release_date'],
                                end_date=cleaned_data['end_date'], series=cleaned_data['series'])
                    card.save()
                return self.form_valid(form)
            else:
                return self.form_invalid(form)


class BonusCardDeleteView(BaseDetailView, UpdateFieldMixin):
    model = Card

    def get_success_url(self) -> str:
        return reverse('all-cards')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        kwargs['field'] = 'deleted'

        if 'delete' in request.POST:
            kwargs['value'] = True
            self.update(self.object, **kwargs)

        return HttpResponseRedirect(self.get_success_url())


class TrashListView(generic.ListView):
    template_name = 'bonus_system/trash.html'
    model = Card
    paginate_by = 5

    def get_queryset(self):
        try:
            q = Card.objects.filter(deleted=True)
        except Card.DoesNotExist:
            return None
        else:
            return q

    def get_paginate_by(self, queryset):
        return self.paginate_by if queryset else None


class TrashDetailView(generic.DetailView, UpdateFieldMixin):
    template_name = 'bonus_system/trash_detail.html'
    model = Card

    def get_success_url(self) -> str:
        return reverse('all-cards')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        kwargs['field'] = 'deleted'

        if 'restore' in request.POST:
            kwargs['value'] = False
            self.update(self.object, **kwargs)

        if 'delete-permanently' in request.POST:
            self.object.delete()

        return HttpResponseRedirect(self.get_success_url())


class SearchListView(generic.ListView):
    model = Card

    def get_queryset(self):
        query = self.request.GET.get('search')
        if query:
            return Card.objects.filter(Q(series__icontains=query)
                                       | Q(number__contains=query)
                                       | Q(release_date__contains=query)
                                       | Q(end_date__contains=query)
                                       | Q(state__icontains=query))


################### RESTAPI ###########################


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'cards': reverse_lazy('card-list', request=request, format=format),
        'orders': reverse_lazy('order-list', request=request, format=format),
        'products': reverse_lazy('product-list', request=request, format=format),
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
        return self.filter_queryset(Card.objects.filter(number=self.kwargs['number'])).first()


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

