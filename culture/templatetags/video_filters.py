from django import template
import re

register = template.Library()

@register.filter
def youtube_embed(url):
    """Конвертирует обычную ссылку YouTube в embed ссылку с параметрами"""
    if not url:
        return ''
    
    url = str(url).strip()
    
    # Проверка для youtube.com/watch?v=ID
    if 'youtube.com/watch?v=' in url:
        try:
            video_id = url.split('v=')[1].split('&')[0].strip()
            if video_id:
                # Добавляем параметры для лучшей совместимости и обхода ошибки 153
                # rel=0 - убирает рекомендованные видео в конце
                # modestbranding=1 - скрывает YouTube логотип
                # fs=1 - явно разрешаем fullscreen
                # controls=1 - явно показываем контролы
                params = 'rel=0&modestbranding=1&fs=1&controls=1'
                return f'https://www.youtube.com/embed/{video_id}?{params}'
        except (IndexError, AttributeError):
            pass
    
    # Проверка для youtu.be/ID
    if 'youtu.be/' in url:
        try:
            video_id = url.split('youtu.be/')[1].split('?')[0].split('&')[0].strip()
            if video_id:
                params = 'rel=0&modestbranding=1&fs=1&controls=1'
                return f'https://www.youtube.com/embed/{video_id}?{params}'
        except (IndexError, AttributeError):
            pass
    
    return url

@register.filter
def vimeo_embed(url):
    """Конвертирует обычную ссылку Vimeo в embed ссылку"""
    if not url:
        return ''
    
    url = str(url).strip()
    
    if 'vimeo.com/' in url:
        try:
            # Извлекаем ID видео
            video_id = url.split('vimeo.com/')[1].split('/')[-1].split('?')[0].strip()
            if video_id and video_id.isdigit():
                return f'https://player.vimeo.com/video/{video_id}'
        except (IndexError, AttributeError):
            pass
    
    return url

@register.filter
def vk_embed(url):
    """Конвертирует обычную ссылку ВКонтакте в embed ссылку"""
    try:
        if not url:
            return ''
        
        url = str(url).strip()
        
        # Поддерживаем оба домена: vk.com и vkvideo.ru
        if 'vk.com/video' not in url and 'vkvideo.ru/video' not in url:
            return url
        
        # Извлекаем oid и id из URL
        # Форматы: 
        # https://vk.com/video-123456_789012
        # https://vkvideo.ru/video-228163754_456240347
        # Используем более точный regex
        match = re.search(r'video(-?\d+)_(\d+)', url)
        if match:
            oid = match.group(1)
            vid = match.group(2)
            # Используем embed URL который работает для обоих доменов
            return f'https://vk.com/video_ext.php?oid={oid}&id={vid}&hd=2'
    except Exception as e:
        import traceback
        traceback.print_exc()
    
    return url

@register.filter
def get_video_platform(url):
    """Определяет платформу видео по URL"""
    if not url:
        return None
    if 'youtube.com' in url or 'youtu.be' in url:
        return 'YouTube'
    elif 'vimeo.com' in url:
        return 'Vimeo'
    elif 'vk.com' in url or 'vkvideo.ru' in url:
        return 'ВКонтакте'

@register.filter
def video_mime_type(file_path):
    """Определяет MIME тип видеофайла по расширению"""
    if not file_path:
        return 'video/mp4'
    
    file_path_str = str(file_path).lower()
    
    if file_path_str.endswith('.mp4'):
        return 'video/mp4'
    elif file_path_str.endswith('.webm'):
        return 'video/webm'
    elif file_path_str.endswith('.ogg') or file_path_str.endswith('.ogv'):
        return 'video/ogg'
    elif file_path_str.endswith('.avi'):
        return 'video/x-msvideo'
    elif file_path_str.endswith('.mov'):
        return 'video/quicktime'
    elif file_path_str.endswith('.mkv'):
        return 'video/x-matroska'
    elif file_path_str.endswith('.flv'):
        return 'video/x-flv'
    elif file_path_str.endswith('.wmv'):
        return 'video/x-ms-wmv'
    
    # По умолчанию
    return 'video/mp4'