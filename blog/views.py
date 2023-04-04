from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import generic, View
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .models import Car, Comment
from .forms import RegistrationForm, CarForm, CommentForm


class Home(View):
    def get(self, request):
        return render(request, "index.html")


class CarGallery(View):
    def get(self, request):
        cars = Car.objects.all()
        context = {"cars": cars}
        return render(request, "car_gallery.html", context)


class LoginView(SuccessMessageMixin, View):
    template_name = "account/login.html"
    success_url = reverse_lazy("home")
    success_message = "You have logged in successfully!"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("home")
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, self.success_message)
            return redirect(self.success_url)
        else:
            messages.error(request, "Invalid username or password!")
            return redirect("login")


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "You have successfully logged out!")
        return redirect("home")


class RegisterView(View):
    def get(self, request):
        return render(request, "account/register.html")

    def post(self, request):

        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()

            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created for {username}")
            return redirect("login")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
        return redirect("register")


class AddPost(View):
    def get(self, request):

        return render(request, "addpost_form.html", {"car_form": CarForm()})

    def post(self, request):

        car_form = CarForm(request.POST, request.FILES)

        if car_form.is_valid():
            Car = car_form.save(commit=False)
            Car.site_user = request.user
            Car.slug = slugify(f"{car.make} {car.model} {car.year}").replace(" ", "-")
            Car.save()
            messages.success(request, "Post has been added Successfully")
            return redirect("cargallery")
        else:
            # CarForm = CarForm()

            return render(request, "addpost_form.html", {"car_form": CarForm})


class ViewCarPost(View):
    def get(self, request, slug):
        car = get_object_or_404(Car, slug=slug)
        comment_form = CommentForm()
        context = {"car": car, "comment_form": comment_form, "user": request.user}
        return render(request, "view_car_post.html", context)

    def post(self, request, slug):
        car = get_object_or_404(Car, slug=slug)
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.car = car
            comment.author = request.user
            comment.save()
            messages.success(request, "Comment Added Successfully")
            return redirect("view_car_post", slug=slug)
        else:
            context = {"car": car, "comment_form": comment_form, "user": request.user}
            return render(request, "view_car_post.html", context)


@require_POST
@login_required
def like_comment(request):
    comment_id = request.POST.get("comment_id")
    action = request.POST.get("action")

    if comment_id and action:
        try:
            comment = Comment.objects.get(id=comment_id)
            if action == "like":
                comment.likes.add(request.user)
            else:
                comment.likes.remove(request.user)
            return JsonResponse({"status": "ok"})
        except:
            pass
        return JsonResponse({"status": "error"})
