from django.shortcuts import render, redirect, get_object_or_404
from .models import shortURL
import string
import random

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

def home(request):
    return render(request, 'shortener/home.html')

def shorten_url(request):
    if request.method == 'POST':
        original_url = request.POST.get('original_url')
        short_code = generate_short_code()

        while shortURL.objects.filter(short_code=short_code).exists():
            short_code = generate_short_code()

        short_url = shortURL.objects.create(original_url=original_url, short_code=short_code)

        return render(request, 'shortener/home.html',{'short_url': request.build_absolute_uri(f'/{short_url.short_code}/')})

    return redirect('home')

def redirect_url(request, short_code):
    short_url = get_object_or_404(shortURL,short_code=short_code)
    short_url.click_count += 1
    short_url.save()

    return redirect(short_url.original_url)