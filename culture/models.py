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
    
    # Унифицировано с UserUpload - используется youtube_url для ссылок на видео
    youtube_url = models.URLField(
        blank=True, 
        null=True, 
        help_text="Ссылка на видео (YouTube, Vimeo, ВКонтакте)"
    )
    video_url = models.URLField(
        blank=True, 
        null=True, 
        help_text="Альтернативная ссылка на видео (для совместимости)"
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

class Award(models.Model):
    """Модель для наград с фотографиями"""
    name = models.CharField(max_length=200, verbose_name="Название награды")
    description = models.TextField(blank=True, verbose_name="Описание")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Категория")
    image = models.ImageField(upload_to='awards/', verbose_name="Фотография награды")
    date = models.DateField(verbose_name="Дата получения")
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = "Награда"
        verbose_name_plural = "Награды"
        ordering = ['-date']
    
    def __str__(self):
        return self.name
    
    def is_user_upload(self):
        return False

# Простая модель для пользовательских загрузок
class UserUpload(models.Model):
    TYPE_CHOICES = [
        ('photo', 'Фотография'),
        ('video', 'Видео'),
        ('poster', 'Афиша'),
        ('award', 'Награда'),
    ]
    
    upload_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    # Категория для пользовательских загрузок (например, награды)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Файлы
    image = models.ImageField(upload_to='user_uploads/images/', blank=True, null=True)
    video = models.FileField(upload_to='user_uploads/videos/', blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.title}"
    
    def is_user_upload(self):
        return True