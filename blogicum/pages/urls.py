# pages/urls.py
# URL-шаблоны приложения pages

from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('<path:path>/', views.FlatPageView.as_view(), name='flatpage'),
]
