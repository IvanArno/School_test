from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('posters/', views.posters_list, name='posters'),
    path('performances/', views.performances_list, name='performances'),
    path('performance/<int:pk>/', views.performance_detail, name='performance_detail'),
    path('photos/', views.photos_list, name='photos'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)