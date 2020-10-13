from django import forms 

from .models import Exercise
# from staff_only.models import Ascription, Composition


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ('date', 'time', 'remarques', 'rating')
        help_texts = {
            'date': ('date in format yyyy-mm-dd')
        }


class PlaceForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ('place', 'place_description')


class DurationForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ('duration',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ('comment',)

class RepetitionForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ('repetitions',)

class ItineraryForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ('itinerary',)

class FlavorForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ('flavor',)



