from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.db import models


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def __str__(self):
        return self.title


class CustomUserManager(BaseUserManager):
    """
    custom user manager for user model with email as the unique identifier
    """

    def create_user(self, username, email, password=None, **extra_fields):
        """
        create and return a regular user with an email and password
        """
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username filed must be set')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fileds):
        """
        create and return a superuser with admin privileges
        """
        extra_fileds.setdefault('is_staff', True)
        extra_fileds.setdefault('is_superuser', True)
        extra_fileds.setdefault('is_active', True)

        if extra_fileds.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fileds.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self.create_user(username, email, password, **extra_fileds)



class User(AbstractUser):
    date_of_birth = models.DateField()
    profile_photo = models.ImageField(upload_to='profile_photos/',
                                      blank=True, null=True)

    objects = CustomUserManager() # Assign the custom manager

    def __str__(self):
        return self.username