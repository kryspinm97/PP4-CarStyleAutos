from django.test import TestCase
from blog.forms import CarForm, RegistrationForm, CommentForm


class RegistrationFormTestCase(TestCase):

    def test_registration_form(self):
        form = RegistrationForm(data={
            'username': 'testuser',
            'email': 'testuser@gmail.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
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
            'car_image': '',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('car_image', form.errors.keys())
        self.assertEqual(form.errors['car_image'][0], 'No file selected!')

    def test_invalid_car_form(self):
        form_data = {
                'make': '',
                'model': '',
                'year': 2020,
                'specifications': 'specs',
                'rundown': 'runs',
        }
        form = CarForm(data=form_data)
        self.assertFalse(form.is_valid())


class TestCommentForm(TestCase):

    def test_comment_form(self):
        form = CommentForm(data={
            'text': 'This is a test comment.',
        })

        self.assertTrue(form.is_valid())

    def test_invalid_comment_form(self):
        form_data = {
            'text': '',
        }
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())
