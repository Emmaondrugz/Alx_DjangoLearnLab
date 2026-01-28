from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


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





# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.PROTECT)

    def __str__(self):
        return self.title

    class Meta:
        # These are custom "Labels" we create for the database
        permissions = [
            ("can_add_book", "Can add book"),
            ("can_change_book", "Can change book"),
            ("can_delete_book", "Can delete book"),
        ]

class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return self.name

class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    # The list of predefined roles
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    ]

    # Link to the built-in User model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.name} - {self.role}"

    # This function runs every time a User object is saved
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()