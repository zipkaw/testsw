# Generated by Django 4.1.6 on 2023-02-15 23:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bonus_system', '0012_alter_card_end_date_alter_card_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 15, 23, 6, 36, 599267, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='card',
            name='release_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 15, 23, 6, 36, 599255, tzinfo=datetime.timezone.utc)),
        ),
    ]
