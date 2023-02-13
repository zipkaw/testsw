from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.urls import reverse


PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]

class Card(models.Model):

    class CardSeries(models.TextChoices):
        STUFF = 'SF', ('Staff card')
        DEFAULT = 'DF', ('Default')
        PRIME = 'PR', ('Prime')

    series = models.CharField(max_length=2, choices=CardSeries.choices)
    number = models.CharField(max_length=16, primary_key=True)
    release_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    last_use_date = models.DateTimeField(null=True, blank=True)
    total_orders = models.IntegerField(default=0)

    class CardStates(models.TextChoices):
        ACTIVED = 'AC', ('Activated')
        NOT_ACTIVATED = 'NA', ('Not activated') 
        OVERDUE = 'OD', ('Overdue')

    state = models.CharField(max_length=2,
                             choices=CardStates.choices,
                             default=CardStates.NOT_ACTIVATED,)

    # orders = models.ForeignKey(Order, on_delete=models.CASCADE)

    discount = models.IntegerField(validators=PERCENTAGE_VALIDATOR, null=True, blank=True)
    deleted = models.BooleanField(verbose_name='Was deleted')

    class Meta:
        pass
    
    def is_active(self):
        return True if self.state == 'AC' else False
    
    def is_overdue(self):
        if timezone.now() > self.end_date.date(): 
            state = self.CardStates.OVERDUE
            return True
        return False

    def is_deleted(self):
        return self.deleted

    def __str__(self) -> str:
        return f'{self.number} bonus card'
    
    def get_absolute_url(self): 
        return reverse('card', kwargs={'pk' : self.pk})
    
    def get_absolute_url_to_delete(self): 
        return reverse('delete-card', kwargs={'pk' : self.pk})

class Order(models.Model):

    num = models.CharField(max_length=50)
    date = models.DateTimeField(null=True, blank=True)
    sell_price = models.IntegerField(null=True, blank=True)
    order_discount = models.IntegerField(validators=PERCENTAGE_VALIDATOR, null=True, blank=True)
    total_discount = models.IntegerField(null=True, blank=True)
    card = models.ForeignKey(Card, on_delete=models.DO_NOTHING)
    
    @property
    def count_discount(self):
        return self.sell_price * (1 - self.order_discount)

    def __str__(self) -> str:
        return f'Order: {self.num}' 


class Product(models.Model):

    order = models.ManyToManyField(Order)
    name = models.CharField(max_length=50)
    price = models.IntegerField(null=True, blank=True)
    discount_cost = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return f'Product: {self.name}'

