from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """
    Custom User model - future-proof for fitness-specific fields


    """

    def __str__(self):
        return self.username
