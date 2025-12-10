from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Poster(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='posters/')
    description = models.TextField()
    date = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.title

class Performance(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    
    # Видео поля
    video_url = models.URLField(
        blank=True, 
        null=True, 
        help_text="Ссылка на YouTube видео (например: https://www.youtube.com/watch?v=VIDEO_ID)"
    )
    video_file = models.FileField(
        upload_to='videos/', 
        blank=True, 
        null=True,
        help_text="Загрузите видео в формате MP4 (рекомендуется)"
    )
    
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.title

class Photo(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='photos/')
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    uploaded_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.title