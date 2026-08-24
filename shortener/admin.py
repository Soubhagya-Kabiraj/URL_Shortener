from django.contrib import admin
from .models import shortURL

@admin.register(shortURL)
class ShortURLAdmin(admin.ModelAdmin):
    list_display = ('id','original_url','short_code','click_count','created_at',)

    search_fields = ('original_url','short_code',)

    list_filter = ('created_at',)