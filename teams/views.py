from django.contrib import messages
# from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView, TemplateView, UpdateView

from .custom_mixins import FullProfileOrStaffMixin, SameUserOnlyMixin
from .forms import (AddressForm, DogForm, LoginForm, UserCreateForm, UserForm)
from .models import User, Dog

# Create your views here.


class HomeView(TemplateView):
    template_name = 'teams/home.html'


class LoginUserView(LoginView):
    template_name = 'teams/login.html'

    def get_success_url(self):
        url = self.get_redirect_url()
        if self.request.user.is_staff:
            return reverse_lazy('staff_only:clients')
        return reverse_lazy(
            'training:profile', kwargs={
                'pk': self.request.user.pk})


class LogoutUserView(LogoutView):
    next_page = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class SingInView(View):
    def get(self, request, *args, **kwargs):
        form = UserCreateForm()
        return render(request, 'teams/sign_in.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request,
                'Account created, but inactive. Please login and complete your profile to activate your account.')
            return redirect('teams:login')
        return render(request, 'teams/sign_in.html', {'form': form})


class ProfileInfoView(View):
    def get(self, request, *args, **kwargs):
        print(request.user)
        print(f'has_full_profile: {request.user.has_full_profile}')
        print(f'is_staff: {request.user.is_staff}')
        user_form = UserForm()
        coordinates_form = CoordinatesForm()
        dog_form = DogForm()
        context = {
            'user_form': user_form,
            'coordinates_form': coordinates_form,
            'dog_form': dog_form,
        }
        return render(request, 'teams/profile_info.html', context)

    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST)
        coordinates_form = CoordinatesForm(request.POST)
        dog_form = DogForm(request.POST)
        if not user_form.is_valid():
            return redirect(reverse('teams:profile_info', kwargs={'pk': request.user.pk}))
#           return render(request, 'teams/profile_info.html', context)
        if not coordinates_form.is_valid():
            return redirect(reverse('teams:profile_info', kwargs={'pk': request.user.pk}))
        if dog_form.is_valid():
            user = request.user
            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']
            user.email = user_form.cleaned_data['email']
            country = coordinates_form.cleaned_data['country']
            zip_code = coordinates_form.cleaned_data['zip_code']
            dog_data = dog_form.cleaned_data
            dog = Dog.objects.create(user=user, **dog_data)
            coordinates = Coordinates.objects.create(user=user, country=country, zip_code=zip_code)
            user.save()
            return redirect(reverse('teams:team_detail', kwargs={'pk': user.pk}))

        return render(request, 'teams/profile_info.html', context)


class TeamView(SameUserOnlyMixin, FullProfileOrStaffMixin, DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'teams/team_detail.html'


class EditProfileView(FullProfileOrStaffMixin, SameUserOnlyMixin, UpdateView):
    model = User
    form_class = UserForm
    second_model = Dog
    second_form_class = DogForm
    template_name = 'teams/team_edit.html'

    def get_context_data(self, **kwargs):
        context = super(EditProfileView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            dog_form = self.second_form_class(self.request.POST, prefix='dog')
        else:
            dog_object = self.second_model.objects.get(user=self.get_object())
            dog_form = self.second_form_class(instance=dog_object, prefix='dog')
        context['dog_form'] = dog_form
        return context

    def post(self, request, *args, **kwargs):
        response = super(EditProfileView, self).post(request, *args, **kwargs)
        dog_form = self.second_form_class(self.request.POST,  prefix='dog')
        if dog_form.is_valid():
            user = self.get_object()
            self.second_model.objects.filter(user=user).update(**dog_form.cleaned_data)
            return response
        return render(request, self.template_name, {
            'form': self.get_form(self.get_form_class()),
            'dog_form': dog_form
        })

 
