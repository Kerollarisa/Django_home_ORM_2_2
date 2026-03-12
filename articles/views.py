from django.views.generic import ListView
from django.shortcuts import render

from articles.models import Article


class ArticleListView(ListView):
    model = Article
    template_name = 'articles/news.html'
    context_object_name = 'object_list'  # Имя переменной в шаблоне
    ordering = '-published_at'
    
    
# Если нужно сохранить функцию для старых URL
def articles_list(request):
    return ArticleListView.as_view()(request)