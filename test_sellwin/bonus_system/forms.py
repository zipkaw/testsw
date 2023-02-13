from django import forms
from django.core.exceptions import ValidationError
from .models import Card


class BonusCardStateForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = (
            'state',
        )
    
