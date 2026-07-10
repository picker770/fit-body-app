import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth import get_user_model

from products.models import Product
from .models import Order, Subscription, MembershipPlan
from .decorators import premium_required

User = get_user_model()


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
    Stripe webhook handler - processes payment confirmations
    """
    stripe.api_key = settings.STRIPE_SECRET_KEY
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET
    
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
    
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        order = Order.objects.filter(
            stripe_payment_intent=session['id']
        ).first()
        if order:
            order.status = 'paid'
            order.save()
        
        subscription_id = session.get('subscription')
        if subscription_id:
            user_id = session.get('metadata', {}).get('user_id')
            if user_id:
                try:
                    user = User.objects.get(id=user_id)
                    subscription, created = Subscription.objects.update_or_create(
                        user=user,
                        defaults={
                            'stripe_subscription_id': subscription_id,
                            'stripe_customer_id': session.get('customer'),
                            'status': 'active',
                        }
                    )
                    # ✅ Fixed: user.profile instead of user.Profile
                    user.profile.membership_status = 'premium'
                    user.profile.save()
                except User.DoesNotExist:
                    pass
    
    elif event['type'] == 'customer.subscription.deleted':
        subscription_obj = event['data']['object']
        subscription = Subscription.objects.filter(
            stripe_subscription_id=subscription_obj['id']
        ).first()
        if subscription:
            subscription.status = 'canceled'
            subscription.save()
            # ✅ Fixed: subscription.user.profile instead of subscription.user.Profile
            subscription.user.profile.membership_status = 'free'
            subscription.user.profile.save()
    
    return HttpResponse(status=200)


@login_required
def subscription_checkout(request, plan_slug):
    """
    Create Stripe Checkout session for subscription
    """
    plan = get_object_or_404(MembershipPlan, slug=plan_slug, is_active=True)
    
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
            subscription_id = session.get('subscription')
            if subscription_id:
                stripe_sub = stripe.Subscription.retrieve(subscription_id)
                
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
                
                # ✅ Fixed: request.user.profile instead of request.user.Profile
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
        stripe.Subscription.modify(
            request.user.subscription.stripe_subscription_id,
            cancel_at_period_end=True
        )
        
        request.user.subscription.status = 'canceled'
        request.user.subscription.save()
        
        # ✅ Fixed: request.user.profile instead of request.user.Profile
        request.user.profile.membership_status = 'free'
        request.user.profile.save()
        
        messages.success(request, 'Your subscription has been cancelled. You will have access until the end of the billing period.')
        
    except Exception as e:
        messages.error(request, f'Error cancelling subscription: {str(e)}')
    
    return redirect('dashboard:home')


@premium_required
def premium_content(request):
    """
    Example view for premium-only content
    """
    return render(request, 'payments/premium_content.html')