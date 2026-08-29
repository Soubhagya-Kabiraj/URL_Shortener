from django.shortcuts import render, redirect, get_object_or_404
from .models import shortURL
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import shortURL

import string
import random

# UPDATED CODE: SnapURL Dashboard Logic
def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')

        user = User.objects.create_user(username=username, password=password)
        login(request, user)

        return redirect('dashboard')

    return render(request,'shortener/register.html')


# UPDATED CODE: SnapURL Dashboard Logic
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        from django.contrib.auth import authenticate
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username,password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        messages.error(request, 'Invalid username or password.')

    return render(request, 'shortener/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

# UPDATED CODE: SnapURL Dashboard Logic
@login_required
def home(request):
    urls = shortURL.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shortener/home.html', {'urls':urls})

# UPDATED CODE: SnapURL Dashboard Logic
@login_required
def shorten_url(request):
    if request.method == 'POST':
        original_url = request.POST.get('original_url')
        short_code = generate_short_code()

        while shortURL.objects.filter(short_code=short_code).exists():
            short_code = generate_short_code()

        short_url = shortURL.objects.create(user=request.user, original_url=original_url, short_code=short_code)

        return redirect('home')

    return redirect('home')

def redirect_url(request, short_code):
    short_url = get_object_or_404(shortURL,short_code=short_code)

    short_url.click_count += 1
    short_url.save(update_fields=['click_count'])

    return redirect(short_url.original_url)

# UPDATED CODE: SnapURL Dashboard Logic
@login_required
def delete_url(request, url_id):
    if request.method == 'POST':
        url = get_object_or_404(shortURL, id=url_id, user=request.user)
        url.delete()

    return redirect('home')

# UPDATED CODE: SnapURL Dashboard Logic
@login_required
def dashboard_view(request):
    user_urls = shortURL.objects.filter(user=request.user)
    total_urls = user_urls.count()
    total_history = total_urls
    recent_activities = user_urls.order_by('-created_at')[:5]
    
    context = {
        'total_urls': total_urls,
        'total_history': total_history,
        'recent_activities': recent_activities,
    }
    return render(request, 'shortener/dashboard.html', context)

# UPDATED CODE: SnapURL Dashboard Logic
@login_required
def history_view(request):
    urls = shortURL.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shortener/history.html', {'urls': urls})