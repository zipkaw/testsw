# Generated by Django 4.1.6 on 2023-02-12 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bonus_system', '0003_rename_cards_card_rename_orders_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='id',
        ),
        migrations.AlterField(
            model_name='card',
            name='number',
            field=models.CharField(default=0, max_length=16, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]