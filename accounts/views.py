from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm, UserUpdateForm, ProfileUpdateForm

User = get_user_model()


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome {user.username}!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


def profile(request, username):  # ✅ Changed from Profile to profile
    user = get_object_or_404(User, username=username)
    return render(request, 'accounts/profile.html', {'profile_user': user})  # ✅ Changed to lowercase


@login_required
def profile_edit(request):  # ✅ Changed from Profile_edit to profile_edit
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)  # ✅ Fixed: lowercase

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Profile updated!')
            return redirect('accounts:profile', username=request.user.username)  # ✅ Fixed: lowercase
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)  # ✅ Fixed: lowercase

    return render(request, 'accounts/profile_edit.html', {'u_form': u_form, 'p_form': p_form})  # ✅ Fixed: lowercase