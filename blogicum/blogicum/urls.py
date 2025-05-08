# Главные URL-шаблоны проекта

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/registration/', include('blog.urls', namespace='registration')),
    path('', include('blog.urls')),
    path('pages/', include('pages.urls')),
]

# Добавление медиафайлов для разработки
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
