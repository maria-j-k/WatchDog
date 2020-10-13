from django.contrib.postgres.fields import HStoreField
from django.db import models

from teams.models import User
# Create your models here.


class Composition(models.Model):
    name = models.CharField(max_length=32)
    instruction = models.TextField()
    field_set = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Ascription(models.Model):
    composition = models.ForeignKey(Composition,
            verbose_name = 'Exercise',
            on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)


    class Meta:
        unique_together = ('composition', 'user',)

    def __str__(self):
        return f'{self.composition}, {self.user}'
