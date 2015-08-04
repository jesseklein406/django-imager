from django import forms
from django.contrib.auth.models import User

from .models import ImagerProfile


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = ImagerProfile
        fields = ('camera', 'address', 'web_url', 'type_photography',)


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

