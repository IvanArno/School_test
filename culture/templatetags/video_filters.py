from django import template
import re

register = template.Library()

@register.filter
def youtube_embed(url):
    """Конвертирует обычную ссылку YouTube в embed ссылку"""
    if 'youtube.com/watch?v=' in url:
        video_id = url.split('v=')[1].split('&')[0]
        return f'https://www.youtube.com/embed/{video_id}'
    elif 'youtu.be/' in url:
        video_id = url.split('youtu.be/')[1].split('?')[0]
        return f'https://www.youtube.com/embed/{video_id}'
    return url

@register.filter
def vimeo_embed(url):
    """Конвертирует обычную ссылку Vimeo в embed ссылку"""
    if 'vimeo.com/' in url:
        video_id = url.split('vimeo.com/')[1].split('/')[-1]
        return f'https://player.vimeo.com/video/{video_id}'
    return url

@register.filter
def vk_embed(url):
    """Конвертирует обычную ссылку ВКонтакте в embed ссылку"""
    try:
        if not url:
            return url
        
        # Поддерживаем оба домена: vk.com и vkvideo.ru
        if 'vk.com/video' not in url and 'vkvideo.ru/video' not in url:
            return url
        
        # Извлекаем oid и id из URL
        # Форматы: 
        # https://vk.com/video-123456_789012
        # https://vkvideo.ru/video-228163754_456240347
        match = re.search(r'video(-?\d+)_(\d+)', url)
        if match:
            oid = match.group(1)
            vid = match.group(2)
            return f'https://vk.com/video_ext.php?oid={oid}&id={vid}'
    except Exception:
        pass
    
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
    return 'Другое'