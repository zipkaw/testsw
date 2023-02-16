from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.timezone import now
from dateutil.relativedelta import relativedelta

from django.urls import reverse


PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]

class Card(models.Model):

    class CardSeries(models.TextChoices):
        STUFF = 'SF', ('Staff card')
        DEFAULT = 'DF', ('Default')
        PRIME = 'PR', ('Prime')
    
    series = models.CharField(max_length=2, choices=CardSeries.choices)
    number = models.CharField(max_length=16, unique=True)
    release_date = models.DateTimeField(default=now())
    end_date = models.DateTimeField(default=now() + relativedelta(month=6))
    last_use_date = models.DateTimeField(null=True, blank=True)
    total_orders = models.IntegerField(default=0, null=True, blank=True)

    class CardStates(models.TextChoices):
        ACTIVED = 'AC', ('Activated')
        NOT_ACTIVATED = 'NA', ('Not activated') 
        OVERDUE = 'OD', ('Overdue')

    state = models.CharField(max_length=2,
                             choices=CardStates.choices,
                             default=CardStates.NOT_ACTIVATED,)

    # orders = models.ForeignKey(Order, on_delete=models.CASCADE)

    discount = models.IntegerField(validators=PERCENTAGE_VALIDATOR, null=True, blank=True)
    deleted = models.BooleanField(verbose_name='Was deleted', default=False, null=True, blank=True)

    class Meta:
        #ordering = ['number']
        get_latest_by = "release_date"
    
    def is_active(self):
        return True if self.state == 'AC' else False
    
    def is_overdue(self):
        if now() > self.end_date.date(): 
            state = self.CardStates.OVERDUE
            return True
        return False

    def is_deleted(self):
        return self.deleted

    def __str__(self) -> str:
        return f'{self.number}'
    
    def get_absolute_url(self): 
        return reverse('card', kwargs={'pk' : self.pk})
    
    def get_url_to_trash(self): 
        return reverse('trash', kwargs={'pk' : self.pk})
    
    def get_absolute_url_to_delete(self): 
        return reverse('delete-card', kwargs={'pk' : self.pk})
    
    def generate_card_number(self):
        pass
    

class Order(models.Model):

    num = models.CharField(max_length=50)
    date = models.DateTimeField(null=True, blank=True)
    sell_price = models.IntegerField(null=True, blank=True)
    order_discount = models.IntegerField(validators=PERCENTAGE_VALIDATOR, null=True, blank=True)
    total_discount = models.IntegerField(null=True, blank=True)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    
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

