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
    path('upload/', views.upload_page, name='upload'),
    path('upload/file/', views.upload_file, name='upload_file'),
    path('upload/<int:pk>/edit/', views.edit_upload, name='edit_upload'),
    path('upload/<int:pk>/delete/', views.delete_upload, name='delete_upload'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)