from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.timezone import now
from dateutil.relativedelta import relativedelta
from django.urls import reverse

from .exeptions import StatusExeption

PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]
MIN_VALUE_VALIDATOR = [MinValueValidator(0)]


def current_date_validarion():
    """Notice: Validator message uses UTC+00:00"""
    return [MinValueValidator(now() - relativedelta(minutes=5)),
            MaxValueValidator(now() + relativedelta(minutes=5))]


class CardSeries(models.TextChoices):
    STUFF = 'SF', ('Staff card')
    DEFAULT = 'DF', ('Default')
    PRIME = 'PR', ('Prime')


class CardStates(models.TextChoices):
    ACTIVED = 'AC', ('Activated')
    NOT_ACTIVATED = 'NA', ('Not activated')
    OVERDUE = 'OD', ('Overdue')


class Card(models.Model):
    series = models.CharField(max_length=2, choices=CardSeries.choices)
    number = models.CharField(max_length=16, unique=True)
    release_date = models.DateTimeField(default=now())
    end_date = models.DateTimeField(default=now() + relativedelta(months=6))
    last_use_date = models.DateTimeField(null=True, blank=True)
    total_orders = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        validators=MIN_VALUE_VALIDATOR)
    state = models.CharField(
        max_length=2,
        choices=CardStates.choices,
        default=CardStates.NOT_ACTIVATED,)
    discount = models.IntegerField(
        validators=PERCENTAGE_VALIDATOR,
        null=True,
        blank=True,
        default=0)
    deleted = models.BooleanField(
        verbose_name='Was deleted',
        default=False,
        null=True,
        blank=True)
    
    @property
    def is_active(self):
        return True if self.state == 'AC' else False

    @property
    def is_overdue(self):
        if now() > self.end_date:
            self.state = CardStates.OVERDUE
            return True
        return False

    @property
    def is_deleted(self):
        return self.deleted

    def __str__(self) -> str:
        return f'{self.number}'

    def get_absolute_url(self):
        return reverse('card', kwargs={'pk': self.pk})

    def get_url_to_trash(self):
        return reverse('trash_detail', kwargs={'pk': self.pk})

    def get_absolute_url_to_delete(self):
        return reverse('delete-card', kwargs={'pk': self.pk})


class Order(models.Model):

    num = models.CharField(max_length=50, unique=True)
    date = models.DateTimeField(
        null=True,
        blank=True,
        validators=current_date_validarion(),
        default=now())
    sell_price = models.FloatField(null=True, blank=True)
    order_discount = models.IntegerField(
        validators=PERCENTAGE_VALIDATOR,
        null=True,
        blank=True,
        default=0)
    total_discount = models.FloatField(
        null=True,
        blank=True,
        validators=MIN_VALUE_VALIDATOR,
        default=0)
    card = models.ForeignKey(to=Card,
                             on_delete=models.CASCADE,
                             to_field='number',
                             related_name='orders')


    def _count_discount(self):
        """
        The method set current discount value for order, corresponds to the
        discount card value and calculate total discount for order
        """
        
        self.total_discount = self.sell_price * (self.card.discount/100)
        self.order_discount = self.card.discount
        return self.total_discount

    @property
    def total_price(self):
        """Return order price with discount"""
        return self.sell_price - self.total_discount
    
    def save(self, *args, **kwargs) -> None:
        """
        Before saving object needed generate 'num' field, 
        pass kwarg with key 'num' and valid value (must be unique)
        """
        if self.card.is_overdue or not self.card.is_active: 
            raise StatusExeption

        if self.num == '':
            self.num = kwargs.pop('num')
        self._count_discount()
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.num


class Product(models.Model):

    order = models.ManyToManyField(
        to=Order,
        related_name='products',
        blank=True)
    name = models.CharField(max_length=50)
    price = models.FloatField(
        null=True,
        blank=True,
        validators=MIN_VALUE_VALIDATOR)
    discount_price = models.FloatField(
        null=True,
        blank=True,
        validators=MIN_VALUE_VALIDATOR,
        default=0)

    def __str__(self) -> str:
        return self.name
