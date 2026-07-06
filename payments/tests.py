from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from products.models import Product
from .models import Order, Subscription, MembershipPlan

User = get_user_model()


class OrderModelTest(TestCase):
    """Test the Order Model"""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            description='A test product',
            price=19.99,
            product_type='exercise',
            is_active=True
        )
        self.order = Order.objects.create(
            user=self.user,
            product=self.product,
            stripe_payment_intent='pi_test_123',
            amount=19.99,
            status='pending'
        )

    def test_order_creation(self):
        self.assertEqual(self.order.user.username, 'testuser')
        self.assertEqual(self.order.product.name, 'Test Product')
        self.assertEqual(self.order.amount, 19.99)
        self.assertEqual(self.order.status, 'pending')

    def test_order_str_method(self):
        expected = 'testuser - Test Product (pending)'
        self.assertEqual(str(self.order), expected)


class MembershipPlanModelTest(TestCase):
    """Test the MembershipPlan Model"""

    def setUp(self):
        self.plan = MembershipPlan.objects.create(
            name='Premium Monthly',
            slug='premium-monthly',
            plan_type='monthly',
            price=19.99,
            stripe_price_id='price_test_123',
            features='Feature 1, Feature 2, Feature 3',
            is_active=True
        )

    def test_membership_plan_creation(self):
        self.assertEqual(self.plan.name, 'Premium Monthly')
        self.assertEqual(self.plan.price, 19.99)
        self.assertTrue(self.plan.is_active)

    def test_membership_plan_get_features_list(self):
        features = self.plan.get_features_list()
        self.assertEqual(len(features), 3)
        self.assertEqual(features[0], 'Feature 1')

    def test_membership_plan_str_method(self):
        self.assertEqual(str(self.plan), 'Premium Monthly (monthly)')


class SubscriptionModelTest(TestCase):
    """Test the Subscription Model"""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.subscription = Subscription.objects.create(
            user=self.user,
            stripe_subscription_id='sub_test_123',
            stripe_customer_id='cus_test_123',
            status='active'
        )

    def test_subscription_creation(self):
        self.assertEqual(self.subscription.user.username, 'testuser')
        self.assertEqual(self.subscription.status, 'active')
        self.assertTrue(self.subscription.is_active())

    def test_subscription_str_method(self):
        self.assertEqual(str(self.subscription), 'testuser - active')


class PaymentCheckoutTest(TestCase):
    """Test the Payment Checkout Views"""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            description='A test product',
            price=19.99,
            product_type='exercise',
            is_active=True
        )

    def test_checkout_view_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('payments:create_checkout_session', kwargs={'product_id': self.product.id}))
        self.assertEqual(response.status_code, 302)  # Redirect to Stripe

    def test_checkout_view_unauthenticated(self):
        response = self.client.get(reverse('payments:create_checkout_session', kwargs={'product_id': self.product.id}))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_payment_success_view_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('payments:success'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'payments/success.html')

    def test_payment_cancel_view_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('payments:cancel'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'payments/cancel.html')
