from django.contrib.postgres.fields import HStoreField
from django.db import models

from teams.models import User
# Create your models here.


class Composition(models.Model):
    """Stores information about exercise type.
    
        name: string, name given to composition
        instruction: multiline string, describing the rules for exercise
        field_set: string containing names of non-mandatory fields of Exercise model which would be included in the form displayed to user while creating new exercise. """
    name = models.CharField(max_length=32)
    instruction = models.TextField()
    field_set = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Ascription(models.Model):
    """Relates composition to user.
        activate: default True. If false, user won't have possibility to add new instances of exercise associated with this particular ascription."""
    composition = models.ForeignKey(Composition,
            verbose_name = 'Exercise',
            on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)


    class Meta:
        unique_together = ('composition', 'user',)

    def __str__(self):
        return f'{self.composition}, {self.user}'
