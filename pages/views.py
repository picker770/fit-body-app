from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data (you can add email sending here later)
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            # For now, just show success message
            messages.success(request, f'Thank you {name}! We will get back to you soon.')
            return redirect('pages:contact')
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, 'pages/contact.html', {'form': form})
    else:
        form = ContactForm()
    
    return render(request, 'pages/contact.html', {'form': form})