# Generated by Django 3.1.2 on 2020-10-05 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0005_user_remember_me'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='remember_me',
        ),
    ]
