from django import template

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
def get_video_platform(url):
    """Определяет платформу видео по URL"""
    if not url:
        return None
    if 'youtube.com' in url or 'youtu.be' in url:
        return 'YouTube'
    elif 'vimeo.com' in url:
        return 'Vimeo'
    return 'Другое'