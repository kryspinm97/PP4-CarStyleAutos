from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django_summernote.fields import SummernoteTextField
from django_summernote.widgets import SummernoteWidget

# Create your models here.


class Car(models.Model):
    """Site User's Cars Model"""
    make = models.CharField(max_length=50, blank=False)
    model = models.CharField(max_length=50, blank=False)
    slug = models.SlugField(max_length=200, unique=True)
    site_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="car_user"
    )
    created_date = models.DateTimeField(auto_now_add=True)
    year = models.PositiveSmallIntegerField()
    specifications = models.TextField()
    rundown = models.TextField()
    car_image = CloudinaryField("image")
    likes = models.ManyToManyField(User, related_name="car_likes", blank=True)

    class Meta:
        """Metadata options for the Car model"""

        ordering = ["-created_date"]

    def __str__(self):
        """String representation of a Car instance"""
        return f"{self.site_user} : {self.model} ({self.year})"

    def like(self, user):
        """ Add a user to the likes of the Car instance """
        self.likes.add(user)

    def get_absolute_url(self):
        """ Get the absolute URL of a car instance """
        return reverse("cargallery")


class Comment(models.Model):
    """Comments on Car Post model"""
    car = models.ForeignKey(Car, on_delete=models.CASCADE,
                            related_name="comments")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="car_comments"
    )
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="comment_likes")

    def __str__(self):
        """ String representation of a Comment instance"""
        return f"{self.author.username} on {self.car}"

    def like(self, user):
        """ Add a user to the likes of the comment instance"""
        self.likes.add(user)

    def unlike(self, user):
        """ Remove a user from the likes of the Comment instance"""
        self.likes.remove(user)
