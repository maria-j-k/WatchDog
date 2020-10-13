from django.contrib import admin

# Register your models here.
from .models import Ascription, Composition

@admin.register(Ascription)
class AscriptionAdmin(admin.ModelAdmin):
    pass

@admin.register(Composition)
class CompositionAdmin(admin.ModelAdmin):
    pass


