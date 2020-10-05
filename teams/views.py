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

from .custom_mixins import FullProfileOnlyMixin, SameUserOnlyMixin
from .forms import AddressForm, DogForm, LoginForm, UserCreateForm, UserForm
from .models import User, Dog

# Create your views here.


class HomeView(TemplateView):
    template_name = 'teams/home.html'


class LoginUserView(LoginView):
    template_name = 'teams/login.html'

    def get_success_url(self):
        url = self.get_redirect_url()
        return reverse_lazy(
            'teams:team_detail', kwargs={
                'pk': self.request.user.pk})


class LogoutUserView(LogoutView):
    next_page = reverse_lazy('teams:home')

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
        user_form = UserForm()
        dog_form = DogForm()
        context = {
            'user_form': user_form,
            'dog_form': dog_form,
        }
        return render(request, 'teams/profile_info.html', context)

    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST)
        dog_form = DogForm(request.POST)
        if user_form.is_valid() and dog_form.is_valid():  
            user = request.user
            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']
            user.email = user_form.cleaned_data['email']
            user.country = user_form.cleaned_data['country']
            user.zip_code = user_form.cleaned_data['zip_code']
            dog_data = dog_form.cleaned_data
            dog = Dog.objects.create(user=user, **dog_data)
            # user.has_full_profile = True
            # user.save()
            return redirect(reverse('teams:team_detail', kwargs={'pk': user.pk}))
            

        print(user_form.errors)
        print(dog_form.errors)
        return render(request, 'teams/profile_info.html', context)


class TeamView(SameUserOnlyMixin, FullProfileOnlyMixin, DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'teams/team_detail.html'


class EditProfileView(FullProfileOnlyMixin, SameUserOnlyMixin, UpdateView):
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

    