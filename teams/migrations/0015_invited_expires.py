# Generated by Django 3.1.2 on 2020-10-22 09:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0014_auto_20201020_1403'),
    ]

    operations = [
        migrations.AddField(
            model_name='invited',
            name='expires',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 29, 9, 40, 3, 120579), editable=False),
        ),
    ]
