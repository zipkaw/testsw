# Generated by Django 4.1.6 on 2023-02-12 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bonus_system', '0004_remove_card_id_alter_card_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='slug',
            field=models.SlugField(default=True),
        ),
    ]