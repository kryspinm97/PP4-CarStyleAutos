from . import views
from django.urls import path

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('car_gallery/', views.CarGallery.as_view(), name='cargallery'),
    path('account/login', views.LoginView.as_view(), name='login'),
    path('account/register', views.RegisterView.as_view(), name='register'),
]