from django.db import models

class Product:
    pass

class Orders(models.Model):
    num = models.IntegerField() 
    date = models.DateTimeField() 
    sum = models.IntegerField() 
    

class Cards(models.Model):

    series = models.CharField(max_length=50)
    number = models.CharField(max_length=16)
    release_date = models.DateTime()
    end_date = models.DateTimeField()
    last_use_date = models.DateTimeField()
    orders_sum = models.IntegerField()

    class CardStates(models.TextChoices):
        ACTIVED = 'AC', _('Activated')
        NOT_ACTIVATED = 'NA', _('Not activated')
        OVERDUE = 'OD', _('Overdue')

    state = models.CharField(max_length=2,
                             choices=CardStates.choices,
                             default=CardStates.NOT_ACTIVATED,)

    current_discount = models.FloatField()
    orders = models.ForeignKey(Orders, on_delete=models.CASCADE) 
    
    class Meta:
        pass

