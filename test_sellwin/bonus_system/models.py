from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]


class Orders(models.Model):
    num = models.CharField(max_length=50)
    date = models.DateTimeField()
    sell_price = models.IntegerField()
    order_discount = models.IntegerField()
    total_discount = models.IntegerField()

    @property
    def count_discount(self):
        return self.sell_price * (1 - self.order_discount)

    def __str__(self) -> str:
        return 'Order:'.join(self.num)


class Product(models.Model):
    order = models.ManyToManyField(Orders)
    name = models.CharField()
    cost = models.IntegerField()
    discount_cost = models.IntegerField()

    def __str__(self) -> str:
        return 'Product:'.join(self.name) + 'with cost:'.join(self.cost)


class Cards(models.Model):

    series = models.CharField(max_length=50)
    number = models.CharField(max_length=16)
    release_date = models.DateTimeField()
    end_date = models.DateTimeField()
    last_use_date = models.DateTimeField()
    total_orders = models.IntegerField()

    class CardStates(models.TextChoices):
        ACTIVED = 'AC', ('Activated')
        NOT_ACTIVATED = 'NA', ('Not activated')
        OVERDUE = 'OD', ('Overdue')

    state = models.CharField(max_length=2,
                             choices=CardStates.choices,
                             default=CardStates.NOT_ACTIVATED,)

    orders = models.ForeignKey(Orders, on_delete=models.CASCADE)
    discount = models.IntegerField()


    class Meta:
        pass
