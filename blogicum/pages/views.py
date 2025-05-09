# pages/views.py
# Представления для статических страниц и ошибок
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView

from .models import Page


def csrf_failure(request, reason="", exception=None):
    """Обработчик CSRF-ошибок."""
    return render(request, 'pages/403csrf.html',
                  {'reason': reason}, status=403)


def page_not_found(request, exception):
    """Обработчик 404 ошибок."""
    return render(request, 'pages/404.html', status=404)


def server_error(request):
    """Обработчик 500 ошибок."""
    return render(request, 'pages/500.html', status=500)


class FlatPageView(DetailView):
    model = Page
    template_name = 'pages/about.html'
    context_object_name = 'page'

    def get_object(self, queryset=None):
        path = self.kwargs['path']
        return get_object_or_404(Page, url=path, is_active=True)
