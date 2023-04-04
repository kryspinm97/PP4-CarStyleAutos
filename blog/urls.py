from . import views
from django.urls import path, include

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("summernote/", include("django_summernote.urls")),
    path("car_gallery/", views.CarGallery.as_view(), name="cargallery"),
    path("account/login", views.LoginView.as_view(), name="login"),
    path("account/register", views.RegisterView.as_view(), name="register"),
    path("account/logout/", views.LogoutView.as_view(), name="logout"),
    path("addpost_form", views.AddPost.as_view(), name="addpost"),
    path("car/<slug:slug>/", views.ViewCarPost.as_view(), name="view_car_post"),
    path('like-comment/<int:pk>/', views.like_comment, name='like_comment'),
]
