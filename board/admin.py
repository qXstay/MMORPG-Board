from django.contrib import admin
from .models import Category, Post, Response
from django.contrib.auth import get_user_model

User = get_user_model()

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'subscribed_to_news')
    list_filter = ('subscribed_to_news',)
    search_fields = ('email', 'first_name', 'last_name')
