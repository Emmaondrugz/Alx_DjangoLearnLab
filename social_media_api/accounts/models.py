from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    bio = models.TextField()
    profile_picture = models.ImageField(blank=True, upload_to='profile_pics/')
    # This ONE field satisfies Step 1 (following field)
    # AND Step 2 (followers relationship via related_name)
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True
    )
    def __str__(self):
        return self.username

