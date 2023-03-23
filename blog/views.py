from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import generic, View
from django.views.generic import ListView, DetailView
from .models import Car, Comment


class Home(View):

    def get(self, request):
        return render(request, 'index.html')


class CarGallery(View):

    def get(self, request):
        return render(request, 'car_gallery.html')


class LoginView(View):

    def get(self, request):
        return render(request, 'account/login.html')


class RegisterView(View):

    def get(self ,request):
        return render(request, 'account/register.html')