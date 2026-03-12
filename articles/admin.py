from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Section, ArticleSection


class ArticleSectionInlineFormset(BaseInlineFormSet):
    def clean(self):
        """Проверяем, что есть один и только один основной раздел"""
        super().clean()
        
        # Считаем количество основных разделов
        main_sections_count = 0
        
        for form in self.forms:
            # Пропускаем удаленные формы
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_main'):
                    main_sections_count += 1
        
        # Проверяем, что есть хотя бы один основной раздел
        if main_sections_count == 0:
            raise ValidationError('Укажите основной раздел')
        
        # Проверяем, что не больше одного основного раздела
        if main_sections_count > 1:
            raise ValidationError('Основным может быть только один раздел')


class ArticleSectionInline(admin.TabularInline):
    model = ArticleSection
    formset = ArticleSectionInlineFormset
    extra = 1
    verbose_name = 'Тематика'
    verbose_name_plural = 'Тематики'


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'published_at', 'display_sections']
    list_filter = ['published_at']
    search_fields = ['title', 'text']
    inlines = [ArticleSectionInline]
    
    def display_sections(self, obj):
        """Отображение разделов в списке статей"""
        sections = obj.sections.select_related('section').all()
        section_names = [s.section.name for s in sections]
        return ", ".join(section_names) if section_names else "Нет разделов"
    
    display_sections.short_description = 'Разделы'
    
    def get_queryset(self, request):
        """Оптимизация запросов к БД"""
        return super().get_queryset(request).prefetch_related('sections__section')


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'article_count']
    search_fields = ['name']
    
    def article_count(self, obj):
        """Количество статей в разделе"""
        return obj.articles.count()
    
    article_count.short_description = 'Количество статей'