from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from blog.models import Car, Comment
from blog.forms import CarForm, CommentForm
from unittest.mock import MagicMock, patch


class HomeViewTestCase(TestCase):

    def test_home_view_should_return_200(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)


class CarGalleryViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_car_gallery_view_should_return_200(self):
        response = self.client.get(reverse('cargallery'))
        self.assertEqual(response.status_code, 200)

    def test_car_gallery_view_should_display_all_cars(self):
        user = User.objects.create(username='testuser')
        car1 = Car.objects.create(
            make='Toyota',
            model='Camry',
            slug='toyota-camry-2020',
            site_user=user,
            year=2020,
            specifications='<p> specs </p>',
            rundown='<p> rundown </p>',
            car_image='car_image.jpg'
        )
        car2 = Car.objects.create(
            make='Mitsubishi',
            model='Evo',
            slug='mitsubishi-evo-2006',
            site_user=user,
            year=2020,
            specifications='<p> specs </p>',
            rundown='<p> rundown </p>',
            car_image='car_image.jpg'
        )
        response = self.client.get(reverse('cargallery'))
        self.assertContains(response, car1.make)
        self.assertContains(response, car1.model)
        self.assertContains(response, car2.make)
        self.assertContains(response, car2.model)


class LoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('login')
        self.user = User.objects.create_user('testuser', 'testuser@gmail.com', 'testpassword123')

    def test_login_view_should_return_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_login_view_should_login_user(self):
        data = {'username': 'testuser', 'password': 'testpassword123'}
        response = self.client.post(self.url, data=data)
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_view_invalid_credentials(self):
        data = {'username': 'testuser', 'password': 'wrongpass'}
        response = self.client.post(self.url, data=data)
        self.assertRedirects(response, reverse('login'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class LogoutViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('logout')
        self.user = User.objects.create_user('testuser', 'testuser@gmail.com', 'testpassword123')

    def test_logout_view_should_logout_user(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('home'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('register')

    def test_register_view_should_return_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_register_view_should_register_user(self):
        data = {'username': 'testuser', 'email': 'testuser@example.com', 'password1': 'testpass', 'password2': 'testpass'}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().username, 'testuser')
        self.assertEqual(User.objects.first().email, 'testuser@example.com')