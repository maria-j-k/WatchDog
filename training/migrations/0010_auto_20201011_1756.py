# Generated by Django 3.1.2 on 2020-10-11 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0009_auto_20201007_0940'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exercise',
            name='film',
        ),
        migrations.AlterField(
            model_name='exercise',
            name='flavor',
            field=models.IntegerField(choices=[(1, 'cinnamon'), (2, 'orange'), (3, 'cloves')], null=True),
        ),
    ]