# Generated by Django 3.1.2 on 2020-10-28 15:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0023_auto_20201023_1300'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='exercise',
            options={'ordering': ['date']},
        ),
    ]
