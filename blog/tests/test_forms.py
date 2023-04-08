from django.test import TestCase
from ..forms import CarForm, RegistrationForm, CommentForm


class RegistrationFormTestCase(TestCase):

    def test_registration_form(self):
        form = RegistrationForm(data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        })

        self.assertTrue(form.is_valid())


class CarFormTestCase(TestCase):

    def test_car_form(self):
        form = CarForm(data={
            'make': 'Toyota',
            'model': 'Camry',
            'year': 2020,
            'specifications': '<p> specs </p>',
            'rundown': '<p> rundownss </p>',
            'car_image': 'car_image.jpg',
        })

        self.assertTrue(form.is_valid())


class TestCommentForm(TestCase):

    def test_comment_form(self):
        form = CommentForm(data={
            'text': 'This is a test comment.',
        })

        self.assertTrue(form.is_valid())
