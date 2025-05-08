# Регистрация моделей в админ-панели

from django.contrib import admin
from .models import Post, Category, Location, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'pub_date', 'is_published', 'category']
    list_filter = ['is_published', 'category']
    search_fields = ['title', 'text']
    list_editable = ['is_published']
    readonly_fields = ['pub_date']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    search_fields = ['title']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'created_at']
    search_fields = ['text']
    readonly_fields = ['created_at']
