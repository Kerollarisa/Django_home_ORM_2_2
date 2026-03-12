from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение',)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-published_at']  # Добавил сортировку

    def __str__(self):
        return self.title
    
    def get_sections_ordered(self):
        """
        Возвращает разделы в нужном порядке:
        сначала основной раздел, затем все остальные по алфавиту
        """
        # Получаем все связи с разделами
        article_sections = self.sections.select_related('section').all()
        
        # Разделяем на основной и остальные
        main_section = None
        other_sections = []
        
        for article_section in article_sections:
            if article_section.is_main:
                main_section = article_section
            else:
                other_sections.append(article_section)
        
        # Сортируем остальные разделы по имени
        other_sections.sort(key=lambda x: x.section.name)
        
        # Формируем результат
        result = []
        if main_section:
            result.append(main_section)
        result.extend(other_sections)
        
        return result


class Section(models.Model):
    name = models.CharField(max_length=128, verbose_name='Раздел')

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'
        ordering = ['name']

    def __str__(self):
        return self.name


class ArticleSection(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='sections')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='articles')
    is_main = models.BooleanField(default=False, verbose_name='Основной')

    class Meta:
        verbose_name = 'Тематика статьи'
        verbose_name_plural = 'Тематики статьи'
        # Гарантируем, что у статьи не будет дублей разделов
        unique_together = [['article', 'section']]
        
    def __str__(self):
        return f'{self.article.title} - {self.section.name}'