from . import views
from django.urls import path

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('car_gallery/', views.CarGallery.as_view(), name='cargallery'),
]