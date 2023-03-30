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
        cars = Car.objects.all()
        context = {'cars': cars}
        return render(request, 'car_gallery.html', context)


class LoginView(View):

    def get(self, request):
        return render(request, 'account/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password!')
            return redirect('login')


class RegisterView(View):

    def get(self, request):
        return render(request, 'account/register.html')

    def post(self, request):

        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('login')
        else:
            messages.error(request, 'Invalid registration details')
            return redirect('register')
