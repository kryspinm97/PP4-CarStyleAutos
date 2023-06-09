from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.views import generic, View
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Car, Comment
from .forms import RegistrationForm, CarForm, CommentForm
from django.utils.text import slugify


class Home(View):
    """
    Renders the home page of the website
    """
    def get(self, request):
        return render(request, "index.html")


class CarGallery(View):
    """
    Renders the car gallery page where all cars posted by users are displayed
    It also implements pagination so that only six cars are displayed per page
    """
    def get(self, request):
        car_list = Car.objects.all()
        paginator = Paginator(car_list, 6)  # Show 6 Cars per page
        page_number = request.GET.get("page")
        cars = paginator.get_page(page_number)
        context = {
            "cars": cars,
        }

        return render(request, "car_gallery.html", context)


class LoginView(SuccessMessageMixin, View):
    """
    Renders the login page where users can enter their credentials
    to log into the website. It also handles the authentication and login
    process and displays appropriate success/error messages
    """
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
    """
    Handles the logout process when a user clicks on the Logout button.
    It logs out the user and redirects them to the home page with a
    success message
    """
    def get(self, request):
        logout(request)
        messages.success(request, "You have successfully logged out!")
        return redirect("home")


class RegisterView(View):
    """
    Renders the registration page where new users can register for an account
    It also handles the registration process and displays appropriate success
    and error messages.
    """
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
                    messages.error(request, f"{error}")
        return redirect("register")


class AddPost(View):
    """
    Handles GET and POST requests for adding a new car post
    """
    def get(self, request):

        return render(request, "addpost_form.html", {"car_form": CarForm()})

    def post(self, request):

        car_form = CarForm(request.POST, request.FILES)

        if car_form.is_valid():
            car = car_form.save(commit=False)
            car.site_user = request.user
            car.slug = slugify(
                f"{car.make} {car.model} {car.year}").replace(" ", "-")
            car.save()
            messages.success(request, "Post has been added Successfully")
            return redirect("cargallery")
        else:
            car_form = CarForm()
            return render(request, "addpost_form.html", {"car_form": car_form})


class ViewCarPost(View):
    """
    Handles GET and POST requests for viewing a car post
    """
    def get(self, request, slug):
        car = get_object_or_404(Car, slug=slug)
        comment_form = CommentForm()
        context = {"car": car, "comment_form": comment_form,
                   "user": request.user}
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
            context = {"car": car, "comment_form": comment_form,
                       "user": request.user}
            return render(request, "view_car_post.html", context)


class DeleteCarView(UserPassesTestMixin, DeleteView):
    """
    Deletes the car post only if authorized.
    """
    model = Car
    success_url = reverse_lazy('home')
    template_name = 'delete.html'

    def test_func(self):
        car = self.get_object()
        if self.request.user.is_superuser:
            return True
        if self.request.user == car.site_user:
            return True
        return False

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        context = {
            'message': 'Post successfully deleted.'

        }
        return render(request, 'delete.html', context=context)


class DeleteCommentView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Deletes a comment only if authorized.
    """
    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)

        if request.user == comment.author or request.user.is_staff:
            comment.delete()
            messages.success(request, "Comment deleted successfully")
        else:
            messages.error(request,
                           "You are not authorized to delete this comment.")

        return redirect("view_car_post", slug=comment.car.slug)

    def test_func(self):
        # Only allow staff or comment author to delete comment
        comment = get_object_or_404(Comment, id=self.kwargs["comment_id"])
        return any((self.request.user == comment.author,
                    self.request.user.is_staff))


class UserPostsListView(ListView):
    """
    Displays all car posts made by a particular user
    """
    model = Car
    template_name = 'site_user_posts.html'
    context_object_name = 'cars'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs['username'])
        return Car.objects.filter(site_user=user).order_by('-created_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_user'] = get_object_or_404(
            User, username=self.kwargs['username'])
        return context


@require_POST
@login_required
def like_comment(request, comment_id):
    """
    Allows logged in users to like or unlike a comment
    """
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.likes.filter(id=request.user.id).exists():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    return redirect('view_car_post', slug=comment.car.slug)


@login_required
@require_POST
def like_car_post(request, car_id):
    """
    Allows logged in users to like or unlike a car post
    """
    car = get_object_or_404(Car, id=car_id)

    if car.likes.filter(id=request.user.id).exists():
        car.likes.remove(request.user)
    else:
        car.likes.add(request.user)
    return redirect('view_car_post', slug=car.slug)


@login_required
def edit_car_post(request, slug):
    """
    Allows authorized users to edit a car post in their Posts page.
    """
    car = get_object_or_404(Car, slug=slug)

    if request.user != car.site_user:
        messages.warning(request, "You can't edit this post.")
        return redirect('home')

    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your car post has been updated!')
            return redirect('view_car_post', slug=car.slug)

    else:
        form = CarForm(instance=car)
        helper = FormHelper()
        helper.add_input(Submit('submit', 'Update Post'))
        form.helper = helper

    context = {
        'form': form,
        'car': car
    }

    return render(request, 'editpost_form.html', context)


def handler404(request, exception):
    """
    Displays a custom 404 error page.
    """
    return render(request, '404.html', status=404)
