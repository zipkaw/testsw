# Generated by Django 4.1.6 on 2023-02-20 21:36

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bonus_system', '0013_alter_card_end_date_alter_card_release_date_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['num']},
        ),
        migrations.AlterField(
            model_name='card',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 20, 21, 36, 53, 273756, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='card',
            name='release_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 20, 21, 36, 53, 273741, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 2, 20, 21, 36, 53, 274195, tzinfo=datetime.timezone.utc), null=True, validators=[django.core.validators.MinValueValidator(datetime.datetime(2023, 2, 20, 21, 31, 53, 274148, tzinfo=datetime.timezone.utc)), django.core.validators.MaxValueValidator(datetime.datetime(2023, 2, 20, 21, 41, 53, 274177, tzinfo=datetime.timezone.utc))]),
        ),
    ]