# culture/models.py
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
    
    def is_user_upload(self):
        return False

class Performance(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    
    video_url = models.URLField(
        blank=True, 
        null=True, 
        help_text="Ссылка на YouTube видео"
    )
    video_file = models.FileField(
        upload_to='videos/', 
        blank=True, 
        null=True,
        help_text="Загрузите видео в формате MP4"
    )
    
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.title
    
    def is_user_upload(self):
        return False

class Photo(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='photos/')
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    uploaded_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.title
    
    def is_user_upload(self):
        return False

# Простая модель для пользовательских загрузок
class UserUpload(models.Model):
    TYPE_CHOICES = [
        ('photo', 'Фотография'),
        ('video', 'Видео'),
        ('poster', 'Афиша'),
    ]
    
    upload_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Файлы
    image = models.ImageField(upload_to='user_uploads/images/', blank=True, null=True)
    video = models.FileField(upload_to='user_uploads/videos/', blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.title}"
    
    def is_user_upload(self):
        return True