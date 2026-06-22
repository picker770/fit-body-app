import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from products.models import Product
from .models import Order, Subscription, MembershipPlan

@login_required
def create_checkout_session(request, product_id):
    """
    Create Stripe Checkout session for one-time product purchase
    """
    product = get_object_or_404(Product, id=product_id, is_active=True)
    
    # Check if user already purchased this product
    if Order.objects.filter(user=request.user, product=product, status='paid').exists():
        messages.info(request, 'You already own this plan!')
        return redirect('products:detail', slug=product.slug)
    
    stripe.api_key = settings.STRIPE_SECRET_KEY
    
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'gbp',
                        'product_data': {
                            'name': product.name,
                            'description': product.description[:200],
                        },
                        'unit_amount': int(product.price * 100),
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=request.build_absolute_uri('/payments/success/') + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri('/payments/cancel/'),
            client_reference_id=str(product.id),
            metadata={
                'product_id': product.id,
                'user_id': request.user.id,
            },
        )

        # Create order with pending status
        Order.objects.create(
            user=request.user,
            product=product,
            stripe_payment_intent=checkout_session.id,
            amount=product.price,
            status='pending'
        )
        
        return redirect(checkout_session.url)
        
    except Exception as e:
        messages.error(request, f'Payment error: {str(e)}')
        return redirect('products:detail', slug=product.slug)
    
@login_required
def payment_success(request):
    """
    Payment success page
    """
    session_id = request.GET.get('session_id')
    if session_id:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            # Update order status
            order = Order.objects.filter(
                stripe_payment_intent=session_id,
                user=request.user
            ).first()
            if order:
                order.status = 'paid'
                order.save()
                messages.success(request, f'Payment successful! You now own "{order.product.name}".')
            else:
                messages.warning(request, 'Payment completed but order not found.')
        except Exception as e:
            messages.error(request, f'Error verifying payment: {str(e)}')
    
    return render(request, 'payments/success.html')

@login_required
def payment_cancel(request):
    """
    Payment cancel page
    """
    messages.warning(request, 'Payment was cancelled.')
    return render(request, 'payments/cancel.html')


@csrf_exempt
def stripe_webhook(request):
    """
    Stripe webhook handler
    """
    stripe.api_key = settings.STRIPE_SECRET_KEY
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET
    
    # If no webhook secret, just return 200 (for development)
    if not webhook_secret:
        return HttpResponse(status=200)
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)
    
    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # Update order status
        order = Order.objects.filter(
            stripe_payment_intent=session['id']
        ).first()
        if order:
            order.status = 'paid'
            order.save()
    
    return HttpResponse(status=200)

@login_required
def subscription_checkout(request, plan_slug):
    """
    Create Stripe Checkout session for subscription
    """
    plan = get_object_or_404(MembershipPlan, slug=plan_slug, is_active=True)
    
    # Check if user already has active subscription
    if hasattr(request.user, 'subscription') and request.user.subscription.is_active():
        messages.info(request, 'You already have an active subscription.')
        return redirect('dashboard:home')
    
    stripe.api_key = settings.STRIPE_SECRET_KEY
    
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': plan.stripe_price_id,
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=request.build_absolute_uri('/payments/subscription/success/') + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri('/payments/subscription/cancel/'),
            client_reference_id=str(plan.id),
            metadata={
                'plan_id': plan.id,
                'user_id': request.user.id,
            },
        )
        
        return redirect(checkout_session.url)
        
    except Exception as e:
        messages.error(request, f'Subscription error: {str(e)}')
        return redirect('pages:pricing')


@login_required
def subscription_success(request):
    """
    Subscription success page
    """
    session_id = request.GET.get('session_id')
    if session_id:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            # Get the subscription from Stripe
            subscription_id = session.get('subscription')
            if subscription_id:
                stripe_sub = stripe.Subscription.retrieve(subscription_id)
                
                # Update or create subscription record
                subscription, created = Subscription.objects.update_or_create(
                    user=request.user,
                    defaults={
                        'stripe_subscription_id': subscription_id,
                        'stripe_customer_id': session.get('customer'),
                        'status': 'active',
                        'current_period_start': stripe_sub.current_period_start,
                        'current_period_end': stripe_sub.current_period_end,
                    }
                )
                
                # Update user profile membership status
                request.user.profile.membership_status = 'premium'
                request.user.profile.save()
                
                messages.success(request, 'Subscription activated! Welcome to Premium.')
            else:
                messages.warning(request, 'Subscription activation in progress.')
        except Exception as e:
            messages.error(request, f'Error verifying subscription: {str(e)}')
    
    return render(request, 'payments/subscription_success.html')


@login_required
def subscription_cancel(request):
    """
    Subscription cancel page
    """
    messages.warning(request, 'Subscription was cancelled.')
    return render(request, 'payments/subscription_cancel.html')


@login_required
def cancel_subscription(request):
    """
    Cancel active subscription
    """
    if not hasattr(request.user, 'subscription') or not request.user.subscription.is_active():
        messages.warning(request, 'You do not have an active subscription.')
        return redirect('dashboard:home')
    
    stripe.api_key = settings.STRIPE_SECRET_KEY
    
    try:
        # Cancel at period end
        stripe.Subscription.modify(
            request.user.subscription.stripe_subscription_id,
            cancel_at_period_end=True
        )
        
        # Update status
        request.user.subscription.status = 'canceled'
        request.user.subscription.save()
        
        # Update profile
        request.user.profile.membership_status = 'free'
        request.user.profile.save()
        
        messages.success(request, 'Your subscription has been cancelled. You will have access until the end of the billing period.')
        
    except Exception as e:
        messages.error(request, f'Error cancelling subscription: {str(e)}')
    
    return redirect('dashboard:home')