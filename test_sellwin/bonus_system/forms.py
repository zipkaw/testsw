from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.http import Http404

from .models import Card


class BonusCardStateForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = (
            'state',
        )


class BonusCardGenerateForm(forms.ModelForm, forms.Form):
    class Meta:
        model = Card
        fields = (
            'series',
            'release_date',
            'end_date',
        )

    card_count = forms.IntegerField()

    def clean_dates(self):
        end_date = self.clean_end_date()
        release_date = self.clean_release_date()
        if release_date >= end_date:
            raise ValidationError(
                'Release date can\'t be geather than end date')

    def get_generated_cards(self) -> list:
        cards = []

        # If Cards object does not exists create cards starting with
        # default number

        DEFAULT_NUM = '0000000000000000'
        count = self.clean()['card_count']

        try:
            card_num = Card.objects.latest('number').number
        except Card.DoesNotExist:
            card_num = DEFAULT_NUM

        cards = self.card_factory(card_num, count)

        return cards

    def card_factory(self, number: str, count: int):
        """
            Card factory provides new list of cards numbers, count of this specifing
            by count argument, card number starts with value more by one.
        """

        # The algorithm convert string in 2-digit number list and then increment
        # last number value. If 2-dig num is geather than 100 algorithm
        # take next 2-digit and make the same opirations. than algorithm convert
        # it to str object and appends to cards list and return it

        cards = []
        num = [int(number[x:x+2]) for x in range(0, len(number), 2)]

        for _ in range(0, count):
            str_num = ''
            for index in range((int(len(number) / 2)) - 1, 0, -1):
                num[index] += 1
                if num[index] >= 100:
                    num[index] = 0
                else:
                    break
            for subnum in num:
                if subnum < 10:
                    str_num += '0'
                str_num += str(subnum)
            cards.append(str_num)

        return cards
