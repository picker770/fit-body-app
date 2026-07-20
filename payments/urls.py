from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    # One-time payments
    path('checkout/<int:product_id>/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.payment_success, name='success'),
    path('cancel/', views.payment_cancel, name='cancel'),
    path('webhook/', views.stripe_webhook, name='webhook'),
    
    # Subscriptions - specific URLs FIRST (before the dynamic one)
    path('subscription/success/', views.subscription_success, name='subscription_success'),
    path('subscription/cancel/', views.subscription_cancel, name='subscription_cancel'),
    path('subscription/end/', views.cancel_subscription, name='cancel_subscription'),
    path('subscription/<slug:plan_slug>/', views.subscription_checkout, name='subscription_checkout'),
]