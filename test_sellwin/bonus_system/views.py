from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import FormMixin
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.urls import reverse

from .forms import BonusCardStateForm
from .models import Card, Order, Product
from .maxin import DeleteToTrashMixin


class BonusCardDetailView(generic.DetailView, FormMixin):
    model = Card
    form_class = BonusCardStateForm

    def get_success_url(self) -> str:
        self.object = self.get_object()
        return reverse('card', args=[self.get_object().pk])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(card = context['card'])
        context['form'] = self.get_form()
        return context
    
    def get_initial(self):
        current_state = self.get_object().state
        return {'state':current_state} 
    def form_valid(self, form):
        self.object = self.get_object()
        cleaned_data = form.cleaned_data
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
    paginate_by = 10


class BonusCreateView(generic.CreateView):
    pass

class BonusCardDelete(DeleteToTrashMixin):

    model = Card
    def get_success_url(self) -> str:
        return reverse('all-cards')

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


