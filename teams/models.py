from datetime import date

from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.urls import reverse

from django_countries.fields import CountryField


def compute_age(birth):
    now = date.today()
    if  birth.month == now.month:
        years = now.year - birth.year
    else:
        years = now.year - birth.year - ((birth.month, birth.day) > (now.month, now.day))
    months = now.month - birth.month if now.month >= birth.month else now.month
    days = now.day - birth.day
    if days < -15:
        if months == 0:
            years -= 1
            months = 11
        else:
            months -= 1
    elif days > 15:
        if months == 11:
            years += 1
            months = 0
        else:
            months += 1
    age = {
        'years': years,
        'months': months
        }
    return age

# Create your models here.
class User(AbstractUser):
    """Stores users.
        _has_full_profile: property enabling access to most of pages. Set to True if user has completed their profile.
        zip_code: postal code provided by user. Needed to find gegraphical coordonates.
        country: provided by user
        lat: latitude took from openweahter api while saving profile detail
        lon : longitude took form openweather api while saving profile detail
        location: nearest city took form openweather api whiel saving profile detail"""

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
    """Stores information about user's dog
        dogs_name: name of dog
        dogs_birthday: allows calculation of dogs age at given moment
        dogs_bread: bread of dog
        team_description: anything user would like to add, especially problems with dog's behavior, the problem they want to work on, etc."""
#    def user_directory_path(instance, filename):
#        return 'profile_pic/user_{0}/{1}'.format(instance.user.id, filename)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dogs_name = models.CharField(max_length=32)
    # dogs_pic = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    dogs_birthday = models.DateField()
    dogs_bread = models.CharField(max_length=64)
    team_description = models.TextField()

    @property
    def age(self):
        self._age = compute_age(self.dogs_birthday)
        return self._age


