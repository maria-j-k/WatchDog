from datetime import date

from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.urls import reverse

from django_countries.fields import CountryField



# Create your models here.
class User(AbstractUser):

    # def user_directory_path(instance, filename):
    #     return 'profile_pic/user_{0}/{1}'.format(instance.user.id, filename)

    # profile_pic = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    _has_full_profile = models.BooleanField(default=False)
    zip_code = models.CharField(max_length=10)
    country = CountryField()
    offset = models.IntegerField(null=True)
    lat = models.IntegerField(null=True)
    lon = models.IntegerField(null=True)
    location = models.CharField(max_length=255, null=True)

    def get_absolute_url(self):
        return reverse('teams:team_detail', args=[str(self.id)])

    @property
    def has_full_profile(self):
        self._has_full_profile = False
#       if all([self.coordinates and self.dog]):
        if all([self.country and self.dog]):
            self._has_full_profile = True
        self.save()
        return self._has_full_profile


#class Coordinates(models.Model):
#    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
#    lat = models.IntegerField(null=True)
#    lon = models.IntegerField(null=True)
#    city = models.CharField(max_length=255, null=True)


class Dog(models.Model):
    def user_directory_path(instance, filename):
        return 'profile_pic/user_{0}/{1}'.format(instance.user.id, filename)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dogs_name = models.CharField(max_length=32)
    # dogs_pic = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
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

