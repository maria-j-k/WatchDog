# Generated by Django 3.1.2 on 2020-10-23 20:18

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0022_auto_20201023_1802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invited',
            name='expires',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 30, 20, 18, 15, 989836, tzinfo=utc), editable=False),
        ),
    ]