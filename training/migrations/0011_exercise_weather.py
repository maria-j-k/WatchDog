# Generated by Django 3.1.2 on 2020-10-13 12:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0010_auto_20201011_1756'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercise',
            name='weather',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='training.weather'),
        ),
    ]
