from django.shortcuts import render, redirect, get_object_or_404
from .models import shortURL
import string
import random

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

def home(request):
    urls = shortURL.objects.all().order_by('-created_at')
    return render(request, 'shortener/home.html', {'urls':urls})

def shorten_url(request):
    if request.method == 'POST':
        original_url = request.POST.get('original_url')
        short_code = generate_short_code()

        while shortURL.objects.filter(short_code=short_code).exists():
            short_code = generate_short_code()

        short_url = shortURL.objects.create(original_url=original_url, short_code=short_code)

        return redirect('home')

    return redirect('home')

def redirect_url(request, short_code):
    short_url = get_object_or_404(shortURL,short_code=short_code)

    short_url.click_count += 1
    short_url.save(update_fields=['click_count'])

    return redirect(short_url.original_url)

def delete_url(request, url_id):
    if request.method == 'POST':
        url = get_object_or_404(shortURL, id=url_id)
        url.delete()

    return redirect('home')