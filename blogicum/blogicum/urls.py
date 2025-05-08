# Главные URL-шаблоны проекта

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),  # Подключение URL для авторизации
    path('', include('blog.urls')),
    path('pages/', include('pages.urls')),
]
