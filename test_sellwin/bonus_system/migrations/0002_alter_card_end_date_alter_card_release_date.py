# Generated by Django 4.1.6 on 2023-02-16 10:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bonus_system', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 16, 10, 31, 16, 301641, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='card',
            name='release_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 16, 10, 31, 16, 301641, tzinfo=datetime.timezone.utc)),
        ),
    ]