from django.core.management.base import BaseCommand
from django.utils import timezone

from teams.models import Invited

class Command(BaseCommand):
    help = 'Destroys invited objects when invitation expired'

    def handle(self, *args, **kwargs):
        print(Invited.objects.filter(expires__lte=timezone.now()).delete())
