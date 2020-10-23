from django import forms 
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User 

from django_countries.fields import CountryField

from .models import  Dog, Invited, User


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
#   profile_pic = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email','country', 'zip_code', 'profile_pic')

#class CoordinatesForm(forms.ModelForm):
#    class Meta:
#        model = Coordinates
#        fields = ('country', 'zip_code')

class AddressForm(forms.ModelForm):
    country = CountryField(blank_label='(select country)')

    class Meta:
        model = User
        fields = ('zip_code', 'country')


class DogForm(forms.ModelForm):
    country = CountryField(blank_label='(select country)')

    class Meta:
        model = Dog
        fields = ('dogs_name', 'dogs_birthday', 'dogs_pic',
            'dogs_bread', 'team_description')


class InviteForm(forms.Form):
    email = forms.CharField(max_length=254)
