# culture/views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.middleware.csrf import get_token
from django.utils import timezone
import json
from .models import Poster, Performance, Photo, Category, UserUpload

def home(request):
    # Берем материалы из основных моделей
    posters = Poster.objects.all().order_by('-date')[:3]
    performances = Performance.objects.all().order_by('-date')[:3]
    photos = Photo.objects.all().order_by('-uploaded_at')[:6]
    
    # И пользовательские загрузки
    user_uploads = UserUpload.objects.all().order_by('-created_at')[:3]
    
    context = {
        'posters': posters,
        'performances': performances,
        'photos': photos,
        'user_uploads': user_uploads,
    }
    return render(request, 'culture/home.html', context)

def posters_list(request):
    # Показываем и официальные афиши и пользовательские
    official_posters = Poster.objects.all().order_by('-date')
    user_posters = UserUpload.objects.filter(upload_type='poster').order_by('-created_at')
    
    # Объединяем
    all_posters = list(official_posters) + list(user_posters)
    
    return render(request, 'culture/posters.html', {'posters': all_posters})

def performances_list(request):
    # Показываем и официальные представления и пользовательские видео
    official_performances = Performance.objects.all().order_by('-date')
    user_performances = UserUpload.objects.filter(upload_type='video').order_by('-created_at')
    
    # Объединяем
    all_performances = list(official_performances) + list(user_performances)
    
    return render(request, 'culture/performances.html', {'performances': all_performances})

def performance_detail(request, pk):
    try:
        # Сначала ищем в официальных
        performance = Performance.objects.get(pk=pk)
    except Performance.DoesNotExist:
        # Если нет, ищем в пользовательских
        performance = get_object_or_404(UserUpload, pk=pk)
    
    return render(request, 'culture/performance_detail.html', {'performance': performance})

def photos_list(request):
    # Показываем и официальные фото и пользовательские
    official_photos = Photo.objects.all().order_by('-uploaded_at')
    user_photos = UserUpload.objects.filter(upload_type='photo').order_by('-created_at')
    
    # Объединяем
    all_photos = list(official_photos) + list(user_photos)
    categories = Category.objects.all()
    
    return render(request, 'culture/photos.html', {
        'photos': all_photos,
        'categories': categories
    })

def upload_page(request):
    return render(request, 'culture/upload.html')

@require_http_methods(["POST"])
def upload_file(request):
    try:
        upload_type = request.POST.get('type', 'photo')
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        youtube_url = request.POST.get('youtube_url', '').strip()
        
        # Логирование для отладки
        print(f"Upload attempt - Type: {upload_type}, Title: {title}, Video URL: {youtube_url}")
        print(f"Files: {list(request.FILES.keys())}")
        
        # Проверяем обязательные поля
        if not title:
            return JsonResponse({
                'success': False,
                'error': 'Название материала обязательно'
            }, status=400)
        
        # Проверяем для видео
        if upload_type == 'video':
            if not youtube_url and 'video' not in request.FILES:
                return JsonResponse({
                    'success': False,
                    'error': 'Загрузите видеофайл или введите ссылку на видео'
                }, status=400)
        
        # Создаем пользовательскую загрузку
        upload = UserUpload.objects.create(
            upload_type=upload_type,
            title=title,
            description=description,
            youtube_url=youtube_url if youtube_url else None,
        )
        
        # Обрабатываем файлы
        if 'photo_image' in request.FILES:
            upload.image = request.FILES['photo_image']
        elif 'poster_image' in request.FILES:
            upload.image = request.FILES['poster_image']
        if 'video' in request.FILES:
            upload.video = request.FILES['video']
        
        upload.save()
        
        # Автоматически создаем запись в соответствующем разделе
        if upload_type == 'poster' and upload.image:
            # Создаем афишу
            Poster.objects.create(
                title=title,
                image=upload.image,
                description=description,
                date=timezone.now().date(),
            )
        elif upload_type == 'photo' and upload.image:
            # Создаем фото
            Photo.objects.create(
                title=title,
                image=upload.image,
                description=description,
            )
        elif upload_type == 'video':
            # Создаем представление
            if upload.video or upload.youtube_url:
                Performance.objects.create(
                    title=title,
                    description=description,
                    date=timezone.now(),
                    video_file=upload.video if upload.video else None,
                    video_url=upload.youtube_url if upload.youtube_url else None,
                )
                print(f"Performance created: {title}")
        
        return JsonResponse({
            'success': True,
            'message': 'Материал успешно загружен и сразу добавлен на сайт!',
            'upload_id': upload.id
        })
        
    except Exception as e:
        import traceback
        error_msg = str(e)
        traceback.print_exc()
        print(f"Upload error: {error_msg}")
        return JsonResponse({
            'success': False,
            'error': error_msg
        }, status=400)