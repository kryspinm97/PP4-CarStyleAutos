from django import forms
from .models import Car
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django_summernote.widgets import SummernoteWidget


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User

        fields = ["username", "email", "password1", "password2"]


class CarForm(forms.ModelForm):
    class Meta:

        model = Car
        fields = ('make', 'model', 'year', 'specifications', 'rundown', 'car_image')
        widgets = {
            'specifications': SummernoteWidget(),
            'rundown': SummernoteWidget(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['car_image'].required = True