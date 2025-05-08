# Представления приложения pages

from django.views.generic import TemplateView


class FlatPageView(TemplateView):
    """Обработка статических страниц с помощью CBV"""

    def get_template_names(self):
        return [f'pages/{self.kwargs["path"]}.html']
