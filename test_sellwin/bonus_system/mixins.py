from django.views.generic.edit import FormMixin, UpdateView
from django.views.generic.detail import BaseDetailView
from django.http import HttpResponseRedirect
from django.db import models


class UpdateFieldsMixin:
    """
        Update object field specified in the kwags['field_name'] with value spec. 
        in kwargs['value']
    """
    @staticmethod
    def update(object, **kwargs):
        for field, value in kwargs.items():
            object.__setattr__(field, value)
        object.save()
