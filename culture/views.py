from django.shortcuts import render, get_object_or_404
from .models import Poster, Performance, Photo, Category

def home(request):
    context = {
        'posters': Poster.objects.all().order_by('-date')[:3],
        'performances': Performance.objects.all().order_by('-date')[:3],
        'photos': Photo.objects.all().order_by('-uploaded_at')[:6],
    }
    return render(request, 'culture/home.html', context)

def posters_list(request):
    posters = Poster.objects.all().order_by('-date')
    return render(request, 'culture/posters.html', {'posters': posters})

def performances_list(request):
    performances = Performance.objects.all().order_by('-date')
    return render(request, 'culture/performances.html', {'performances': performances})

def performance_detail(request, pk):
    performance = get_object_or_404(Performance, pk=pk)
    return render(request, 'culture/performance_detail.html', {'performance': performance})

def photos_list(request):
    photos = Photo.objects.all().order_by('-uploaded_at')
    categories = Category.objects.all()
    return render(request, 'culture/photos.html', {
        'photos': photos,
        'categories': categories
    })