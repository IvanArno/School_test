from django.contrib import admin
from .models import Poster, Performance, Photo, Category

@admin.register(Poster)
class PosterAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'created_at']
    list_filter = ['date']
    search_fields = ['title', 'description']

@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'has_video', 'created_at']
    list_filter = ['date']
    search_fields = ['title', 'description']
    
    def has_video(self, obj):
        """Проверяет наличие видео"""
        return bool(obj.video_url or obj.video_file)
    has_video.boolean = True
    has_video.short_description = 'Есть видео'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'uploaded_at']
    list_filter = ['category', 'uploaded_at']
    search_fields = ['title', 'description']