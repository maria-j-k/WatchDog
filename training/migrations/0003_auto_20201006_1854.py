# Generated by Django 3.1.2 on 2020-10-06 18:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0002_exercise_composition'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exercise',
            old_name='flavours',
            new_name='flavor',
        ),
    ]