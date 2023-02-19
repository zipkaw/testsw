# Generated by Django 4.1.6 on 2023-02-19 17:38

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bonus_system', '0010_alter_card_options_alter_card_end_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='discount_cost',
        ),
        migrations.AddField(
            model_name='product',
            name='discount_price',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='card',
            name='discount',
            field=models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='card',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 19, 17, 38, 41, 728396, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='card',
            name='release_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 19, 17, 38, 41, 728396, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(datetime.datetime(2023, 2, 19, 17, 33, 41, 729037, tzinfo=datetime.timezone.utc)), django.core.validators.MaxValueValidator(datetime.datetime(2023, 2, 19, 17, 43, 41, 729065, tzinfo=datetime.timezone.utc))]),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_discount',
            field=models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_discount',
            field=models.FloatField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='product',
            name='order',
            field=models.ManyToManyField(blank=True, related_name='products', to='bonus_system.order'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]