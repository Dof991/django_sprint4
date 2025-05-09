# pages/urls.py
# URL-шаблоны приложения pages

from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('about/', views.FlatPageView.as_view(), name='about'),
    path('rules/',
         views.FlatPageView.as_view(template_name='pages/rules.html'),
         name='rules'),
    path('<path:path>/', views.FlatPageView.as_view(), name='flatpage'),
]
