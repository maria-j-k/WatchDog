from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from staff_only.models import Ascription
from teams.models import User


# Create your models here.
class Weather(models.Model):
    """Collects weather condition data from external api and saves with
    conneciotn to exercise instance."""
    temp = models.IntegerField()
    feels_like = models.IntegerField()
    overall = models.CharField(max_length=32)
    pressure = models.IntegerField()
#   humidity = models.IntegerField()
    wind = models.IntegerField()
#   sunrise = models.DateTimeField()
#   sunset = models.DateTimeField()


def no_future_exercises(date):
    now = timezone.now()
    if date > now:
        raise ValidationError('You\'ve entered future date of your exercise')


class Exercise(models.Model):
    """Stores information about each performance of an exercise. Related to
    user and to composition through ascription."""
    VERY_BAD = -2
    BAD = -1
    NEUTRAL = 0
    GOOD = 1
    VERY_GOOD = 2
    RATING_CHOICES = [
        (VERY_BAD, 'Very bad'),
        (BAD, 'Bad'),
        (NEUTRAL, 'Average'),
        (GOOD, 'Good'),
        (VERY_GOOD, 'Very good'),
    ]
    CINNAMON = 1
    ORANGE = 2
    CLOVES = 3
    FLAVOR_CHOICES = [
        (CINNAMON, 'cinnamon'),
        (ORANGE, 'orange'),
        (CLOVES, 'cloves') ,
    ]

    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, editable=False, on_delete=models.CASCADE)
    last_modified = models.DateTimeField(auto_now=True)
    ascription = models.ForeignKey(Ascription, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    when= models.DateTimeField(validators=[no_future_exercises])
    time = models.CharField(max_length=32, null=True)
    rating = models.IntegerField(choices=RATING_CHOICES, default=NEUTRAL)
    remarques = models.TextField('Additional remarques')
    # photo = models.ImageField(blank=True)
    film = models.URLField('nagranie', blank=True, null=True)
    comment = models.TextField('Instructor\'s comments', null=True)
    duration = models.PositiveIntegerField(null=True)
    repetitions = models.SmallIntegerField(null=True)
    itinerary = models.TextField(null=True)
    place = models.CharField(max_length=32, null=True)
    place_description = models.CharField(max_length=128, null=True)
    flavor = models.IntegerField(choices=FLAVOR_CHOICES, null=True)
    weather = models.OneToOneField(Weather, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['-when']

    def __str__(self):
        return self.ascription.composition.name


