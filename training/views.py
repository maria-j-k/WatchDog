from datetime import datetime, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.generic import DetailView, View

from .forms import (DurationForm, ExerciseForm, FlavorForm,
    ItineraryForm, PlaceForm, RepetitionForm)
from .models import Exercise
from staff_only.models import Ascription, Composition
from teams.models import User
from teams.custom_mixins import SameUserOnlyMixin, FullProfileOrStaffMixin, SameUserOrStaffMixin
from training.utils import check_location, check_current

class HomeView(LoginRequiredMixin, FullProfileOrStaffMixin,
UserPassesTestMixin, View):
    """Displays welcome page for authorised user."""
    def test_func(self):
        """Prevents users who are not staf members form seeing somebody's else
        records."""
        return (self.request.user.pk == self.kwargs['pk']) or (self.request.user.is_staff)

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['pk'])
        context = {
            'user': user,
            'ascription_list': Ascription.objects.filter(user=user.pk)
        }
        return render(request, 'training/home.html', context)


class ExerciseAddView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.kwargs['pk'] in (x.pk for x in self.request.user.ascription_set.all())

    def get(self, request, *args, **kwargs):
        ascription = get_object_or_404(Ascription, pk=kwargs['pk'])
        extra_fields = ascription.composition.extra_fields.split(', ')
        context = {
            'ascription': ascription,
            'form': ExerciseForm(),
        }
        if 'duration' in extra_fields:
            context['duration_form'] = DurationForm()
        if 'place' in  extra_fields:
            context['place_form'] = PlaceForm()
        if 'repetitions' in  extra_fields:
            context['repetitions_form'] = RepetitionForm()
        if 'itinerary' in extra_fields:
            context['itinerary_form'] = ItineraryForm()
        if 'flavor' in extra_fields:
            context['flavor_form'] = FlavorForm()
        return render(request, 'training/exercise_add.html', context)

    def post(self, request, *args, **kwargs):
        ascription = Ascription.objects.get(pk=kwargs['pk'])
        form = ExerciseForm(request.POST)
        data = {}
        if form.is_valid():
            weather = check_current(request.user)
            if weather == None:
                print('Weather is none')## TODO alert message
            data.update(form.cleaned_data)
            place_form = PlaceForm(request.POST)
            duration_form = DurationForm(request.POST)
            repetitions_form = RepetitionForm(request.POST)
            itinerary_form = ItineraryForm(request.POST)
            flavor_form = FlavorForm(request.POST)

            if place_form.is_valid():
                data.update(place_form.cleaned_data)
            if duration_form.is_valid():
                data.update(duration_form.cleaned_data)
            if repetitions_form.is_valid():
                data.update(repetitions_form.cleaned_data)
            if itinerary_form.is_valid():
                data.update(itinerary_form.cleaned_data)
            if flavor_form.is_valid():
                data.update(flavor_form.cleaned_data)
            exercise = Exercise.objects.create(owner=request.user, ascription=ascription, weather=weather, **data)
            return redirect(reverse('training:profile', kwargs={'pk': ascription.user_id}))
        print(form.errors)
        return render(request, 'training/exercise_add.html', {'from': form}) ### TODO dlaczego nie wyświetla mi formularza, jeśli były błędy?


class AscriptionDetailView(UserPassesTestMixin, DetailView):
    """Displays detail of exercises connected with a composition ascribed to
    the user."""
    def test_func(self):
        same_user = self.kwargs['pk'] in (x.pk for x in self.request.user.ascription_set.all())
        return same_user or request.user.is_staff
    model = Ascription
    template_name = 'training/exercises_list.html'

class LocationView(SameUserOnlyMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        check_location(user)
        print(user.location)
        return redirect(reverse('training:profile', kwargs={'pk': request.user.pk}))


