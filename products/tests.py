from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Product, ExercisePlan, NutritionPlan, ProductPurchase

User = get_user_model()


class ProductModelTest(TestCase):
    """Test the Product Model"""

    def setUp(self):
        self.product = Product.objects.create(
            name='Test Workout',
            slug='test-workout',
            description='A test workout plan',
            price=19.99,
            product_type='exercise',
            is_active=True
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Test Workout')
        self.assertEqual(self.product.price, 19.99)
        self.assertEqual(self.product.product_type, 'exercise')
        self.assertTrue(self.product.is_active)

    def test_product_str_method(self):
        self.assertEqual(str(self.product), 'Test Workout')

    def test_product_get_absolute_url(self):
        self.assertEqual(self.product.get_absolute_url(), '/products/test-workout/')

    def test_product_get_product_type_display(self):
        self.assertEqual(self.product.get_product_type_display(), 'Exercise Plan')


class ExercisePlanModelTest(TestCase):
    """Test the ExercisePlan Model"""

    def setUp(self):
        self.product = Product.objects.create(
            name='Test Exercise Plan',
            slug='test-exercise-plan',
            description='A test exercise plan',
            price=29.99,
            product_type='exercise',
            is_active=True
        )
        self.exercise = ExercisePlan.objects.create(
            product=self.product,
            duration_weeks=8,
            difficulty='intermediate',
            equipment_needed='Dumbbells, Mat',
            workouts_per_week=4
        )

    def test_exercise_plan_creation(self):
        self.assertEqual(self.exercise.product.name, 'Test Exercise Plan')
        self.assertEqual(self.exercise.duration_weeks, 8)
        self.assertEqual(self.exercise.difficulty, 'intermediate')

    def test_exercise_plan_str_method(self):
        self.assertEqual(str(self.exercise), 'Exercise: Test Exercise Plan')


class NutritionPlanModelTest(TestCase):
    """Test the NutritionPlan Model"""

    def setUp(self):
        self.product = Product.objects.create(
            name='Test Nutrition Plan',
            slug='test-nutrition-plan',
            description='A test nutrition plan',
            price=24.99,
            product_type='nutrition',
            is_active=True
        )
        self.nutrition = NutritionPlan.objects.create(
            product=self.product,
            meal_type='vegetarian',
            calories_target=2000,
            protein_grams=150,
            carbs_grams=250,
            fats_grams=70
        )

    def test_nutrition_plan_creation(self):
        self.assertEqual(self.nutrition.product.name, 'Test Nutrition Plan')
        self.assertEqual(self.nutrition.calories_target, 2000)
        self.assertEqual(self.nutrition.meal_type, 'vegetarian')

    def test_nutrition_plan_str_method(self):
        self.assertEqual(str(self.nutrition), 'Nutrition: Test Nutrition Plan')


class ProductListViewTest(TestCase):
    """Test the Product List View"""

    def setUp(self):
        Product.objects.create(
            name='Exercise Plan 1',
            slug='exercise-1',
            description='Test exercise',
            price=19.99,
            product_type='exercise',
            is_active=True
        )
        Product.objects.create(
            name='Nutrition Plan 1',
            slug='nutrition-1',
            description='Test nutrition',
            price=24.99,
            product_type='nutrition',
            is_active=True
        )

    def test_product_list_view(self):
        response = self.client.get(reverse('products:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_list.html')
        self.assertEqual(len(response.context['products']), 2)

    def test_product_list_filter_by_type_exercise(self):
        response = self.client.get(reverse('products:list') + '?type=exercise')
        self.assertEqual(len(response.context['products']), 1)
        self.assertEqual(response.context['products'][0].product_type, 'exercise')

    def test_product_list_filter_by_type_nutrition(self):
        response = self.client.get(reverse('products:list') + '?type=nutrition')
        self.assertEqual(len(response.context['products']), 1)
        self.assertEqual(response.context['products'][0].product_type, 'nutrition')

    def test_product_list_search(self):
        response = self.client.get(reverse('products:list') + '?search=Exercise')
        self.assertEqual(len(response.context['products']), 1)


class ProductDetailViewTest(TestCase):
    """Test the Product Detail View"""

    def setUp(self):
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            description='A test product',
            price=19.99,
            product_type='exercise',
            is_active=True
        )

    def test_product_detail_view(self):
        response = self.client.get(reverse('products:detail', kwargs={'slug': 'test-product'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_detail.html')
        self.assertEqual(response.context['product'].name, 'Test Product')

    def test_product_detail_view_nonexistent(self):
        response = self.client.get(reverse('products:detail', kwargs={'slug': 'nonexistent'}))
        self.assertEqual(response.status_code, 404)


