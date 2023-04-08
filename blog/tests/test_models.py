from django.test import TestCase
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Car, Comment


class CarModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.car = Car.objects.create(
            make='Toyota',
            model='Camry',
            slug='toyota-camry-2020',
            site_user=self.user,
            year=2020,
            specifications='<p> specs </p>',
            rundown='<p> rundown </p>',
            car_image='car_image.jpg'
        )

    def test_car_creation(self):
        self.assertEqual(self.car.site_user.username, 'testuser')
        self.assertEqual(self.car.model, 'Camry')
        self.assertEqual(self.car.year, 2020)

    def test_car_like_method(self):
        self.car.like(self.user)
        self.assertTrue(self.user in self.car.likes.all())

    def test_car_str_method(self):
        self.assertEqual(str(self.car), 'testuser : Camry (2020)')

    def test_get_absolute_url(self):
        self.assertEqual(self.car.get_absolute_url(), reverse('cargallery'))

    def test_invalid_car_data(self):
        with self.assertRaises(ValidationError):
            car = Car.objects.create(
                make='',
                model='',
                site_user=self.user,
                year=2020,
                specifications='<p> specs </p>',
                rundown='<p> rundown </p>',
                )
            car.full_clean()


class CommentModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        self.car = Car.objects.create(
            make='Toyota',
            model='Camry',
            slug='toyota-camry-2020',
            site_user=self.user,
            year=2020,
            specifications='<p> specs </p>',
            rundown='<p> rundown </p>',
            car_image='car_image.jpg'
        )

        self.comment = Comment.objects.create(
            car=self.car,
            author=self.user,
            text='This is a test comment.'
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.author.username, 'testuser')
        self.assertEqual(self.comment.car, self.car)
        self.assertEqual(self.comment.text, 'This is a test comment.')

    def test_comment_like_method(self):
        self.comment.like(self.user)
        self.assertTrue(self.user in self.comment.likes.all())

    def test_comment_unlike_method(self):
        self.comment.like(self.user)
        self.comment.unlike(self.user)
        self.assertFalse(self.user in self.comment.likes.all())

    def test_comment_str_method(self):
        self.assertEqual(str(self.comment), 'testuser on testuser : Camry (2020)')
