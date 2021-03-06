# Generated by Django 3.1.2 on 2020-10-06 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0004_remove_exercise_composition'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='comment',
            field=models.TextField(null=True, verbose_name="Instructor's comments"),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='duration',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='flavor',
            field=models.IntegerField(choices=[(1, 'cynamon'), (2, 'pomarańcz'), (3, 'goździki')], null=True),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='itinerary',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='place',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='place_description',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='repetitions',
            field=models.SmallIntegerField(null=True),
        ),
    ]
