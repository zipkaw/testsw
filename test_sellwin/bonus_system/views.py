from django.views import generic
from django.views.generic.edit import FormMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.detail import BaseDetailView
from django.db.models import Q, Prefetch
from django.utils import timezone

from .forms import BonusCardStateForm, BonusCardGenerateForm
from .mixins import UpdateFieldsMixin

from core.models import Card, Order, Product


class BonusCardDetailView(generic.DetailView, FormMixin):
    model = Card
    form_class = BonusCardStateForm
    template_name = 'bonus_system/card_detail.html'

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
    template_name = 'bonus_system/card_list.html'

    def get_queryset(self):
        queryset_to_update = Card.objects.filter(end_date__lt=timezone.now())
        if queryset_to_update:
            queryset_to_update.update(state='OD')
        queryset = Card.objects.filter(deleted = False)
        return queryset


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
                    card = Card(
                        number=card_num,
                        release_date=cleaned_data['release_date'],
                        end_date=cleaned_data['end_date'],
                        series=cleaned_data['series'],
                        state=cleaned_data['state'],
                        discount=cleaned_data['discount'],
                    )
                    card.save()
                return self.form_valid(form)
            else:
                return self.form_invalid(form)


class BonusCardDeleteView(BaseDetailView, UpdateFieldsMixin):
    model = Card

    def get_success_url(self) -> str:
        return reverse('all-cards')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if 'delete' in request.POST:
            kwargs['deleted'] = True
            kwargs['state'] = 'NA'
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


class TrashDetailView(generic.DetailView, UpdateFieldsMixin):
    template_name = 'trash_detail.html'
    model = Card

    def get_success_url(self) -> str:
        return reverse('all-cards')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if 'restore' in request.POST:
            kwargs['deleted'] = False
            self.update(self.object, **kwargs)

        if 'delete-permanently' in request.POST:
            self.object.delete()

        return HttpResponseRedirect(self.get_success_url())


class SearchListView(generic.ListView):
    model = Card

    def get_queryset(self):
        query = self.request.GET.get('search')
        if query:
            return Card.objects.filter(
                Q(series__icontains=query)
                | Q(number__contains=query)
                | Q(release_date__contains=query)
                | Q(end_date__contains=query)
                | Q(state__icontains=query))
