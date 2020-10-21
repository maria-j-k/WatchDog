from django import forms
from django.contrib.auth.models import Permission

from .models import Ascription, Composition
from teams.models import User


class MakeStaffForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=False, is_active=True))
    permission= forms.ModelMultipleChoiceField(
        label='Permissions',
        queryset=Permission.objects.filter(codename__startswith='c_'),
        widget=forms.CheckboxSelectMultiple
    )



class AscriptionForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=False, is_active=True))
    composition = forms.ModelMultipleChoiceField(
        label='Exercise',
        queryset=Composition.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )


class AscribeCompositionForm(forms.Form):
#    composition = forms.ModelChoiceField(queryset=Composition.objects.all())
    users = forms.ModelMultipleChoiceField(
        label='Clients',
        queryset=User.objects.filter(is_staff=False, is_active=True),
        widget=forms.CheckboxSelectMultiple
    )


class ComposeForm(forms.ModelForm):
    class Meta:
        model = Composition
        fields = ('name', 'instruction')


FIELD_CHOICES =(
    ("comment", "instuctor's comment"),
    ("duration", "duration"),
    ("repetitions", "repetitions"),
    ("itinerary", "itinerary"),
    ('place', 'place'),
    ('flavor', 'flavor')
)


class FieldForm(forms.Form):
    field_set = forms.MultipleChoiceField(choices = FIELD_CHOICES, label='Additional parameters', widget=forms.CheckboxSelectMultiple())

