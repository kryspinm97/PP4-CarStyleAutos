from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import generic, View
from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .models import Car, Comment
from .forms import RegistrationForm, CarCreationForm


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
        username = request.POST.get('username')
        password = request.POST.get('password')
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
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
        return redirect('register')

@login_required
def create_car(request):
    if request.method == 'POST':
        form = CarCreationForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.site_user = request.user
            car.save()
            messages.success(request, 'Car Added Successfuly')
            return redirect('car_detail', pk=car.pk)
        else:
            messages.error(request, 'Invalid car details')
    else:
        form = CarCreationForm()
    return render(request, 'create_car.html', {'form': form})