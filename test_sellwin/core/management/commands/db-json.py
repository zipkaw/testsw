
from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.core import serializers

from typing import Any, Optional
import os.path
import os
import json

from core.models import Card, Order, Product

FILE_NAME = '_db_data.json'
FILE_DIR = './test_data_json/'


class Command(BaseCommand):
    help = 'Use this command to fill database test data or get json from database'

    @staticmethod
    def model_to_json(ModelObject: Card | Order | Product, model_name: str):
        """
        Module parses models get all instances and output each model 
        JSON represintation in file '{model_name}_obj_db_data.json'
        """
        queryset = ModelObject.objects.all()
        json_data = serializers.serialize('json', queryset)
        with open(FILE_DIR + FILE_NAME.join([model_name, '']), 'w') as file:
            file.write(json_data)

    @staticmethod
    def json_to_model(ModelObject: Card | Order | Product, model_name: str):
        """
        Module parses '{model_name}_obj_db_data.json' and save objects in database'
        """
        with open(FILE_DIR + FILE_NAME.join([model_name, '']), 'r') as file:
            json_data = json.load(file)
            json_string = json.dumps(json_data)
            for obj in serializers.deserialize('json', json_string):
                obj.save(save_m2m=True)

    def add_arguments(self, parser):
        parser.add_argument(
            '--fill',
            action='store_true',
            help=f'Fill data base with json data from {FILE_DIR}',
        )
        parser.add_argument(
            '--get',
            action='store_true',
            help=f'Get data from database and convert it in json data in {FILE_DIR}',
        )

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        if options['get']:
            self.model_to_json(Card, 'card_obj')
            self.model_to_json(Order, 'order_obj')
            self.model_to_json(Product, 'product_obj')
        elif options['fill']:
            self.json_to_model(Card, 'card_obj')
            self.json_to_model(Order, 'order_obj')
            self.json_to_model(Product, 'product_obj')
