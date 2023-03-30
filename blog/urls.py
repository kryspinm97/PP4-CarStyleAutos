from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('car_gallery/', views.CarGallery.as_view(), name='cargallery'),
    path('account/login', views.LoginView.as_view(), name='login'),
    path('account/register', views.RegisterView.as_view(), name='register'),
]