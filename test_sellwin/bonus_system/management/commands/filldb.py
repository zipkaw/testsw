from django.core.management.base import BaseCommand, CommandError, CommandParser

from typing import Any, Optional
import os.path
import os

from ...models import Card, Order, Product

FILE_NAME = '_data_dict.py'
FILE_PATH = os.getcwd() + FILE_NAME


def model_parser(ModelObject: Card | Order | Product, model_name: str):
    """
    Module parses models get all instances and output each model dictionary represintation 
    in file 'data_dict.py'
    """
    queryset = ModelObject.objects.all()
    with open(FILE_NAME, 'a') as file:
        file.write(f'{model_name}=[',)
        for obj in queryset:
            obj_dict = obj.__dict__
            file.write('{')
            for key, value in obj_dict.items():
                if key != '_state':
                    file.write(f'\'{key}\': \'{value}\',')
            file.write('},\n')
        file.write(']\n')


class Command(BaseCommand):
    help = 'Use this command to fill database test data'

    # def add_arguments(self, parser: CommandParser) -> None:
    #     parser.add_argument('filldb',)

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        if not os.path.exists(FILE_PATH):
            model_parser(Card, 'card_obj')
            model_parser(Order, 'order_obj')
            model_parser(Product, 'product_obj')
