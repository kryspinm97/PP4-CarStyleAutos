from django.test import TestCase
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
