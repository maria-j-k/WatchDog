# Generated by Django 3.1.2 on 2020-10-23 13:00

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import teams.models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0018_auto_20201023_0825'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to=teams.models.User.user_directory_path),
        ),
        migrations.AlterField(
            model_name='invited',
            name='expires',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 30, 13, 0, 31, 457490, tzinfo=utc), editable=False),
        ),
    ]
