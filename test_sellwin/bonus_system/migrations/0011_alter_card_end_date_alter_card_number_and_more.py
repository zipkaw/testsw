# Generated by Django 4.1.6 on 2023-02-15 22:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bonus_system', '0010_alter_card_deleted_alter_card_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 15, 22, 39, 40, 985289, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='card',
            name='number',
            field=models.CharField(max_length=16, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='release_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 15, 22, 39, 40, 985276, tzinfo=datetime.timezone.utc)),
        ),
    ]
