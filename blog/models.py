from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django_summernote.fields import SummernoteTextFormField

# Create your models here.


class Car(models.Model):
    """Site User's Cars"""

    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True)
    site_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="car_user"
    )
    created_date = models.DateTimeField(auto_now_add=True)
    year = models.IntegerField()
    specifications = models.TextField()
    rundown = models.TextField()
    car_image = CloudinaryField("image")
    likes = models.ManyToManyField(User, related_name="car_likes", blank=True)

    class Meta:
        """List posts in a descending order"""

        ordering = ["-created_date"]

    def __str__(self):
        """Generating a title"""
        return f"{self.site_user} : {self.model} ({self.year})"

    def like(self, user):
        self.likes.add(user)

    def get_absolute_url(self):
        return reverse("gallery")


class Comment(models.Model):
    """Comments on Car Post"""

    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="car_comments"
    )
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="comment_likes")

    def __str__(self):
        return f"{self.author.username} on {self.car}"

    def like(self, user):
        self.likes.add(user)

    def unlike(self, user):
        self.likes.remove(user)
