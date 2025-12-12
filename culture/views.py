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
    official_posters = list(Poster.objects.all().order_by('-date')[:5])
    official_performances = list(Performance.objects.all().order_by('-date')[:5])
    official_photos = list(Photo.objects.all().order_by('-uploaded_at')[:10])
    
    # И пользовательские загрузки
    user_posters = list(UserUpload.objects.filter(upload_type='poster').order_by('-created_at')[:5])
    user_performances = list(UserUpload.objects.filter(upload_type='video').order_by('-created_at')[:5])
    user_photos = list(UserUpload.objects.filter(upload_type='photo').order_by('-created_at')[:10])
    
    # Объединяем и сортируем по дате
    all_posters = official_posters + user_posters
    all_posters.sort(key=lambda x: getattr(x, 'date', getattr(x, 'created_at', timezone.now())), reverse=True)
    
    all_performances = official_performances + user_performances
    all_performances.sort(key=lambda x: getattr(x, 'date', getattr(x, 'created_at', timezone.now())), reverse=True)
    
    all_photos = official_photos + user_photos
    all_photos.sort(key=lambda x: getattr(x, 'uploaded_at', getattr(x, 'created_at', timezone.now())), reverse=True)
    
    # Берем только первые 3 для отображения на главной
    posters = all_posters[:3]
    performances = all_performances[:3]
    photos = all_photos[:6]
    
    # И отдельно пользовательские загрузки для секции
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
        
        # Не создаём автоматические записи в Poster/Photo/Performance
        # Пользовательские загрузки отображаются напрямую из UserUpload
        
        return JsonResponse({
            'success': True,
            'message': 'Материал успешно загружен!',
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


def edit_upload(request, pk):
    """Редактирование пользовательской загрузки"""
    try:
        upload = get_object_or_404(UserUpload, pk=pk)
        
        if request.method == 'POST':
            # Обновляем данные
            upload.title = request.POST.get('title', upload.title).strip()
            upload.description = request.POST.get('description', '').strip()
            upload.youtube_url = request.POST.get('youtube_url', '').strip() or None
            
            # Обновляем файлы если они загружены
            if 'image' in request.FILES:
                # Удаляем старый файл если он есть
                if upload.image:
                    upload.image.delete()
                upload.image = request.FILES['image']
            
            if 'video' in request.FILES:
                # Удаляем старый файл если он есть
                if upload.video:
                    upload.video.delete()
                upload.video = request.FILES['video']
            
            upload.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Материал успешно обновлен!',
                'upload_id': upload.id
            })
        
        # GET запрос - показываем форму редактирования
        return render(request, 'culture/edit_upload.html', {'upload': upload})
        
    except UserUpload.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Материал не найден'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


def delete_upload(request, pk):
    """Удаление пользовательской загрузки"""
    try:
        upload = get_object_or_404(UserUpload, pk=pk)
        
        if request.method == 'POST':
            # Удаляем файлы
            if upload.image:
                upload.image.delete()
            if upload.video:
                upload.video.delete()
            
            # Удаляем саму загрузку
            upload.delete()
            
            return JsonResponse({
                'success': True,
                'message': 'Материал успешно удален!',
                'redirect': '/'
            })
        
        # GET запрос - показываем подтверждение удаления
        return render(request, 'culture/delete_upload.html', {'upload': upload})
        
    except UserUpload.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Материал не найден'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)