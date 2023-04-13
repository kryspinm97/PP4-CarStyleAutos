from django import forms
from .models import Car, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django_summernote.fields import SummernoteTextField


class RegistrationForm(UserCreationForm):
    """
    A form for registering a new user
    Inherits from UserCreationForm provided by Django
    """
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class CarForm(forms.ModelForm):
    """
    A form for creating or updating a car post
    """
    class Meta:

        model = Car
        fields = ('make', 'model', 'year',
                  'specifications', 'rundown', 'car_image')
        widgets = {
            'specifications': SummernoteWidget(),
            'rundown': SummernoteWidget(),
        }

    def __init__(self, *args, **kwargs):
        """

        Constructor for CarForm
        Sets car_image field as required

        """
        super().__init__(*args, **kwargs)
        self.fields['car_image'].required = True


class CommentForm(forms.ModelForm):
    """
    A form for creating a comment on a car post
    """

    text = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Leave a comment...',
        'rows': 3,
    }), label='')

    class Meta:
        model = Comment
        fields = ['text']
