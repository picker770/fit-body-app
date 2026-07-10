from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.shortcuts import redirect


def premium_required(view_func):
    """
    Decorator to restrict access to premium users only
    """
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please login to access premium content.')
            return redirect('accounts:login')
        
        if request.user.Profile.membership_status != 'premium':
            messages.warning(request, 'This content is for premium members only.')
            return redirect('pages:pricing')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def subscription_active_required(view_func):
    """
    Decorator to check if user has an active subscription
    """
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please login to access this content.')
            return redirect('accounts:login')
        
        if not hasattr(request.user, 'subscription') or not request.user.subscription.is_active():
            messages.warning(request, 'Please subscribe to access this content.')
            return redirect('pages:pricing')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper