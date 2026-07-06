from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Profile


User = get_user_model()


class CustomUserModelTest(TestCase):
    """Test the Custom User Model"""

    def test_create_user(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)

    def test_user_str_method(self):
        user = User.objects.create_user(username='testuser', password='testpass123')
        self.assertEqual(str(user), 'testuser')


class ProfileModelTest(TestCase):
    """Test the Profile Model"""

    def test_profile_created_on_user_creation(self):
        user = User.objects.create_user(username='testuser', password='testpass123')
        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_profile_str_method(self):
        user = User.objects.create_user(username='testuser', password='testpass123')
        profile = user.profile
        self.assertEqual(str(profile), "testuser's Profile")

    def test_profile_default_values(self):
        user = User.objects.create_user(username='testuser', password='testpass123')
        profile = user.profile
        self.assertEqual(profile.bio, '')
        self.assertEqual(profile.fitness_goal, 'general')
        self.assertEqual(profile.membership_status, 'free')
        self.assertEqual(profile.profile_pic, None)


class RegistrationViewTest(TestCase):
    """Test the Registration View"""

    def test_register_view_get(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_register_view_post_valid(self):
        response = self.client.post(reverse('accounts:register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'Testpass123!',
            'password2': 'Testpass123!',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after registration
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertTrue(Profile.objects.filter(user__username='newuser').exists())

    def test_register_view_post_invalid(self):
        response = self.client.post(reverse('accounts:register'), {
            'username': '',
            'email': 'invalid-email',
            'password1': 'pass',
            'password2': 'pass',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='').exists())

    def test_register_view_post_duplicate_email(self):
        User.objects.create_user(username='existing', email='existing@example.com', password='testpass123')
        response = self.client.post(reverse('accounts:register'), {
            'username': 'newuser',
            'email': 'existing@example.com',
            'password1': 'Testpass123!',
            'password2': 'Testpass123!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'already registered')


class LoginViewTest(TestCase):
    """Test the Login View"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_login_view_get(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_view_post_valid(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after login

    def test_login_view_post_invalid(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please enter a correct username and password')


class ProfileViewTest(TestCase):
    """Test the Profile View"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_profile_view_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('accounts:profile', kwargs={'username': 'testuser'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')

    def test_profile_view_unauthenticated(self):
        response = self.client.get(reverse('accounts:profile', kwargs={'username': 'testuser'}))
        self.assertEqual(response.status_code, 200)  # Profile is public

    def test_profile_view_nonexistent_user(self):
        response = self.client.get(reverse('accounts:profile', kwargs={'username': 'nonexistent'}))
        self.assertEqual(response.status_code, 404)

    def test_profile_edit_view_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('accounts:profile_edit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile_edit.html')

    def test_profile_edit_view_unauthenticated(self):
        response = self.client.get(reverse('accounts:profile_edit'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

