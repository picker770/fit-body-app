from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse 

User = get_user_model()


class Product(models.Model):
    """
    Base Product model - inherited by ExercisePlan and NutritionPlan
    
    """

    PRODUCT_TYPES = [
        ('exercise', 'Exercise Plan'),
        ('nutrition', 'Nutrition Plan'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPES)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'slug': self.slug})

    def get_product_type_display(self):
        return dict(self.PRODUCT_TYPES).get(self.product_type, self.product_type)


class ExercisePlan(models.Model):
    
    """
    Exercise Plan - extends Product with exercise-specific fields

    """
    DIFFICULTY_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    product = models.OneToOneField(
        Product, 
        on_delete=models.CASCADE,
        related_name='exercise_details'
    )
    duration_weeks = models.PositiveBigIntegerField(help_text="Duration in weeks")
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS, default='beginner')
    equipment_needed = models.TextField(blank=True, help_text="List of equipment required")
    workouts_per_week = models.PositiveBigIntegerField(default=3)
    calories_burn_estimate = models.PositiveBigIntegerField(blank=True, null=True, help_text="Estimated calories burned per session")

    def __str__(self):
        return f"Exercise: {self.product.name}"
    
    def get_difficulty_display(self):
        return dict(self.DIFFICULTY_LEVELS).get(self.difficulty, self.difficulty)


class NutritionPlan(models.Model):
    """
    Nutrition Plan - extends Product with nutrition-specific-fields
    """
    MEAL_TYPES = [
        ('vegetarian', 'Vegetarian'),
        ('vegan', 'Vegan'),
        ('keto', 'Keto'),
        ('paleo', 'Paleo'),
        ('mediterranean', 'Mediterranean'),
        ('standard', 'Standard')
    ]

    product = models.OneToOneField(
        Product, 
        on_delete=models.CASCADE,
        related_name='nutrition_details'
    )
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPES, default='standard')
    calories_target = models.PositiveIntegerField(help_text="Daily calorie target")
    protein_grams = models.PositiveIntegerField(help_text="Daily protein target in grams")
    carbs_grams = models.PositiveIntegerField(help_text="Daily carbs target in grams")
    fats_grams = models.PositiveIntegerField(help_text="Daily fats target in grams")
    dietary_restrictions = models.TextField(blank=True, help_text="List any dietary restrictions")
    
    def __str__(self):
        return f"Nutrition: {self.product.name}"
    
    def get_meal_type_display(self):
        return dict(self.MEAL_TYPES).get(self.meal_type, self.meal_type)
    

class ProductPurchase(models.Model):
    """
    Record of a user purchasing a product
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='purchases')
    stripe_payment_intent = models.CharField(max_length=100, blank=True)
    purchase_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-purchase_date']
        unique_together = ['user', 'product']  # Prevent duplicate purchases

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.purchase_date.date()})"
