from django.views.generic.edit import FormMixin, UpdateView
from django.views.generic.detail import BaseDetailView
from django.http import HttpResponseRedirect
from django.db import models


class UpdateFieldMixin:

    """
        Update object field specified in the kwags['field'] with value spec. 
        in kwargs['value']
    """

    @staticmethod
    def update(object, **kwargs):
        object.__setattr__(kwargs.get('field'), kwargs.get('value'))
        object.save(update_fields=[kwargs.get('field')])
