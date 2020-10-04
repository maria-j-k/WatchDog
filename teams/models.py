from datetime import date
from django.contrib.auth.models import AbstractUser, User 
from django.db import models

from django_countries.fields import CountryField



# Create your models here.
class User(AbstractUser):
    profile_pic = models.ImageField(upload_to='profile_pic', blank=True)
    zip_code = models.CharField(max_length=10)
    country = CountryField()
    has_full_profile = models.BooleanField(default=False)


class Dog(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dogs_name = models.CharField(max_length=32)
    dogs_pic = models.ImageField(upload_to='profile_pic', blank=True)
    dogs_birthday = models.DateField()
    dogs_bread = models.CharField(max_length=64)
    team_description = models.TextField()
    

    @property
    def age(self):
        today = date.today()
        years = today.year - self.dogs_birthday.year - \
            ((today.month, today.day) <
             (self.dogs_birthday.month, self.dogs_birthday.day))
        months = today.month - self.dogs_birthday.month
        if months < 0:
            months = 12 + months
        days = today.day - self.dogs_birthday.day
        if days > 15:
            months += 1
        if months == 12:
            months -= 12
            years += 1
        self._age = {
            'years': years,
            'months': months
        }

        return self._age

    def __str__(self):
        return f'{self.user.username} i {self.dogs_name}'
