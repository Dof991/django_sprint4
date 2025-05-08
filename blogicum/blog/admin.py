from django.contrib import admin

from .models import Category, Location, Post


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "is_published", "created_at")
    list_editable = ("is_published",)
    search_fields = ("name",)
    list_filter = ("is_published",)
    fields = ("name", "is_published", "created_at")
    readonly_fields = ("created_at",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "is_published", "created_at")
    list_editable = ("is_published",)
    search_fields = ("title",)
    list_filter = ("is_published",)
    prepopulated_fields = {"slug": ("title",)}
    fields = ("title", "description", "slug", "is_published", "created_at")
    readonly_fields = ("created_at",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "pub_date",
        "author",
        "category",
        "is_published",
        "created_at",
    )
    list_editable = ("is_published",)
    search_fields = ("title", "text")
    list_filter = ("is_published", "pub_date", "author", "category")
    fields = (
        "title",
        "text",
        "pub_date",
        "author",
        "location",
        "category",
        "is_published",
        "created_at",
    )
    readonly_fields = ("created_at",)
    autocomplete_fields = ["author", "location", "category"]
