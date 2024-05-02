from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    MALE = 'M'
    FEMALE ="F"
    OTHER = "O"
    UNDISCLOSED = "U"

    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
        (UNDISCLOSED, 'Undisclosed'),
    ]

    user= models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images', default='default_profile_image.jpg')
    gender = models.CharField(max_length= 20, choices = GENDER_CHOICES, default=UNDISCLOSED)

    def __str__(self):
        return self.user.username