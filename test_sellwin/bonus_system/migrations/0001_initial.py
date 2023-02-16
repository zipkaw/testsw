# Generated by Django 4.1.6 on 2023-02-16 10:13

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('series', models.CharField(choices=[('SF', 'Staff card'), ('DF', 'Default'), ('PR', 'Prime')], max_length=2)),
                ('number', models.CharField(max_length=16, unique=True)),
                ('release_date', models.DateTimeField(default=datetime.datetime(2023, 2, 16, 10, 13, 57, 100707, tzinfo=datetime.timezone.utc))),
                ('end_date', models.DateTimeField(default=datetime.datetime(2023, 6, 16, 10, 13, 57, 100723, tzinfo=datetime.timezone.utc))),
                ('last_use_date', models.DateTimeField(blank=True, null=True)),
                ('total_orders', models.IntegerField(blank=True, default=0, null=True)),
                ('state', models.CharField(choices=[('AC', 'Activated'), ('NA', 'Not activated'), ('OD', 'Overdue')], default='NA', max_length=2)),
                ('discount', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('deleted', models.BooleanField(blank=True, default=False, null=True, verbose_name='Was deleted')),
            ],
            options={
                'get_latest_by': 'release_date',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.CharField(max_length=50)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('sell_price', models.IntegerField(blank=True, null=True)),
                ('order_discount', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('total_discount', models.IntegerField(blank=True, null=True)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bonus_system.card')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.IntegerField(blank=True, null=True)),
                ('discount_cost', models.IntegerField(blank=True, null=True)),
                ('order', models.ManyToManyField(to='bonus_system.order')),
            ],
        ),
    ]
