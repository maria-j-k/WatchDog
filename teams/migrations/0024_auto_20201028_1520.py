# Generated by Django 3.1.2 on 2020-10-28 15:20

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0023_auto_20201023_2018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invited',
            name='expires',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 4, 15, 20, 5, 12560, tzinfo=utc), editable=False),
        ),
    ]