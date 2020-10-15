# Generated by Django 3.1.2 on 2020-10-06 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Composition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('instruction', models.TextField()),
                ('field_set', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('date', models.DateField()),
                ('time', models.CharField(max_length=32)),
                ('rating', models.IntegerField(choices=[(-2, 'Very bad'), (-1, 'Bad'), (0, 'Average'), (1, 'Good'), (2, 'Very good')], default=0)),
                ('remarques', models.TextField(verbose_name='Additional remarques')),
                ('film', models.URLField(blank=True, verbose_name='nagranie')),
                ('comment', models.TextField(verbose_name="Instructor's comments")),
                ('duration', models.PositiveIntegerField()),
                ('repetitions', models.SmallIntegerField()),
                ('itinerary', models.TextField()),
                ('place', models.CharField(max_length=32)),
                ('place_description', models.CharField(max_length=128)),
                ('flavours', models.IntegerField(choices=[(1, 'cynamon'), (2, 'pomarańcz'), (3, 'goździki')])),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temp', models.IntegerField()),
                ('feels_like', models.IntegerField()),
                ('overall', models.CharField(max_length=32)),
                ('pressure', models.IntegerField()),
                ('humidity', models.IntegerField()),
                ('wind', models.IntegerField()),
                ('sunrise', models.DateTimeField()),
                ('sunset', models.DateTimeField()),
                ('offset', models.IntegerField()),
                ('location', models.CharField(max_length=128)),
            ],
        ),
    ]