from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import DetailView, View

from .forms import (DurationForm, ExerciseForm, FlavorForm,
    ItineraryForm, PlaceForm, RepetitionForm)
from .models import Exercise
from staff_only.models import Ascription, Composition
from teams.models import User
from teams.custom_mixins import SameUserOnlyMixin


class HomeView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        # return (self.request.user.pk == self.kwargs['pk']) or (self.request.user.is_staff)
        return self.request.user.pk == self.kwargs['pk']

    def get(self, request, *args, **kwargs):
        context = {
            'ascription_list': Ascription.objects.filter(user=request.user)
        }
        print(context)
        return render(request, 'training/home.html', context)


class ExerciseAddView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.kwargs['pk'] in (x.pk for x in self.request.user.ascription_set.all())

    def get(self, request, *args, **kwargs):
        ascription = get_object_or_404(Ascription, pk=kwargs['pk'])
        field_set = ascription.composition.field_set.split(', ')
        context = {
            'form': ExerciseForm(),
        }
        if 'duration' in field_set:
            context['duration_form'] = DurationForm()
        if 'place' in field_set:
            context['place_form'] = PlaceForm()
        if 'repetitions' in field_set:
            context['repetitions_form'] = RepetitionForm()
        if 'itinerary' in field_set:
            context['itinerary_form'] = ItineraryForm()
        if 'flavor' in field_set:
            context['flavor_form'] = FlavorForm()
        return render(request, 'training/exercise_add.html', context)

    def post(self, request, *args, **kwargs):
        ascription = Ascription.objects.get(pk=kwargs['pk'])
#       ascription = get_object_or_404(Ascription, pk=kwargs['pk'])
        form = ExerciseForm(request.POST)
        data = {}
        if form.is_valid():
            data.update(form.cleaned_data)
            place_form = PlaceForm(request.POST or None)
            duration_form = DurationForm(request.POST or None)
            repetitions_form = RepetitionForm(request.POST or None)
            itinerary_form = ItineraryForm(request.POST or None)
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
            exercise = Exercise.objects.create(owner=request.user,
                ascription=ascription, **data)
            return redirect(reverse('training:exercises', kwargs={'pk': ascription.user_id}))
#           return render(request, 'training/home.html')
        return render(request, 'training/exercise_add.html', {'from': form})


class AscriptionDetailView(DetailView):
    model = Ascription
    template_name = 'training/exercises_list.html'


