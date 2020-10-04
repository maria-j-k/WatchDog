from django import forms 
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User 

from django_countries.fields import CountryField

from .models import User, Dog


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')


class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ('username', 'password1','password2')
        model = User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'profile_pic', )


class AddressForm(forms.ModelForm):
    country = CountryField(blank_label='(select country)')
    class Meta:
        model = User 
        fields = ('zip_code', 'country')


class DogForm(forms.ModelForm):
    country = CountryField(blank_label='(select country)')
    class Meta:
        model = Dog
        fields = ('dogs_name', 'dogs_birthday', 
            'dogs_bread', 'dogs_pic', 'team_description')


# class RegistrationForm(forms.ModelForm):
#     country = CountryField(blank_label='(select country)')
#     password = forms.CharField(widget=forms.PasswordInput())

#     class Meta:
#         model = Team
#         fields = ('first_name', 'last_name', 'email',
#             'zip_code', 'country',  'dogs_name', 'dogs_birthday', 'dogs_bread', 
#             'profile_pic', 'dogs_pic', 'team_description')

