from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """
    Custom User model - future-proof for fitness-specific fields


    """

    def __str__(self):
        return self.username

class Profile(models.Model):
    FITNESS_GOALS = [
        ('weight_loss', 'Weight Loss'),
        ('muscle_gain', 'Muscle Gain'),
        ('endurance', 'Endurance'),
        ('flexibility', 'Flexibility'),
        ('general', 'General Fitness'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    fitness_goal = models.CharField(max_length=20, choices=FITNESS_GOALS, default='general', blank=True)
    profile_pic = models.ImageField(upload_to='profiles/', blank=True, null=True)
    membership_status = models.CharField(max_length=20, default='free')
    stripe_sustomer_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"