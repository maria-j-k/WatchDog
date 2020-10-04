from django.contrib import messages
# from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView, TemplateView

from .custom_mixins import FullProfileOnlyMixin, SameUserOnlyMixin
from .forms import AddressForm, DogForm, LoginForm, UserCreateForm, UserForm
from .models import User, Dog

# Create your views here.


class HomeView(TemplateView):
    template_name = 'teams/home.html'


class LoginUserView(LoginView):
    template_name = 'teams/login.html'
    # success_url = reverse_lazy('teams:team_detail')

    def get_success_url(self):
        url = self.get_redirect_url()
        return reverse_lazy(
            'teams:team_detail', kwargs={
                'pk': self.request.user.pk})


class LogoutUserView(LogoutView):
    next_page = reverse_lazy('teams:home')


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

        print(form.errors)
        return render(request, 'teams/sign_in.html', {'form': form})


class ProfileInfoView(View):
    def get(self, request, *args, **kwargs):
        user_form = UserForm()
        address_form = AddressForm()
        dog_form = DogForm()
        context = {
            'user_form': user_form,
            'address_form': address_form,
            'dog_form': dog_form,
        }
        return render(request, 'teams/profile_info.html', context)

    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST)
        address_form = AddressForm(request.POST)
        dog_form = DogForm(request.POST)
        if user_form.is_valid() and address_form.is_valid() and dog_form.is_valid():
            user = request.user
            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']
            user.email = user_form.cleaned_data['email']
            user.country = address_form.cleaned_data['country']
            user.zip_code = address_form.cleaned_data['zip_code']
            user.save()
            dog_data = dog_form.cleaned_data
            dog = Dog.objects.create(user=user, **dog_data)
            if 'profile_pic' in request.FILES:
                user.profile_pic = request.FILES['profile_pic']
            if 'dogs_pic' in request.FILES:
                dog.dogs_pic = request.FILES['dogs_pic']
            dog.save()
            user.has_full_profile = True
            user.save()
            return redirect(reverse('teams:team_detail', kwargs={'pk': user.pk}))
            

        print(user_form.errors)
        print(address_form.errors)
        print(dog_form.errors)
        return redirect('teams:login')


class TeamView(SameUserOnlyMixin, FullProfileOnlyMixin, DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'teams/team_detail.html'

    # def get_object(self, queryset=None):
    #     obj = super(TeamView, self).get_object(queryset=Team.objects.get(user=self.request.user))
    #     return obj


# class PhotoDetail(DetailView):

#     def get_object(self, queryset=None):
#         obj = super(PhotoDetail, self).get_object(queryset=queryset)
#         if obj.user != obj.photoextended.user:
#             raise Http404()
#         return obj
