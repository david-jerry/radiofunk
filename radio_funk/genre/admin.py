from django.contrib import admin
from .models import Genre

@admin.register(User)
class GenreAdmin(admin.ModelAdmin):
    list_display = ["name", "active", "color"]

