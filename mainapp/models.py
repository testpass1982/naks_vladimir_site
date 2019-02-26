from django.db import models
from django.utils import timezone

# Create your models here.
#тут надо создавать модели потом это сделаем вместе
#например чтобы в админке править новости

#щас простой пример покажу
class ContentMixin(models.Model):
    '''base class for Post, Article and Documents'''
    title = models.CharField(u'Название', max_length=200)
    url_code = models.CharField(u'Код ссылки', max_length=30, blank=True, default='НЕ УКАЗАН')
    short_description = models.CharField(
        u'Краткое описание', max_length=200, blank=True)
    #tags = models.ManyToManyField(Tag, verbose_name='Тэги')
    published_date = models.DateTimeField(
        u'Дата публикации', blank=True, null=True)
    created_date = models.DateTimeField(u'Дата создания', default=timezone.now)
    #text = RichTextUploadingField(verbose_name='Текст')
    author = models.ForeignKey(
        'auth.User', verbose_name='Автор', on_delete=models.CASCADE)
    publish_on_main_page = models.BooleanField(
        verbose_name="Опубликовать на главной", default=False)

    class Meta:
        abstract = True


class Post(ContentMixin):
    '''child of contentmixin'''
    #category = models.ForeignKey(
    #    Category, verbose_name='Категория', on_delete=models.CASCADE)
    publish_on_news_page = models.BooleanField(
        verbose_name="Опубликовать в ленте новостей", default=False)
    secondery_main = models.BooleanField(
        verbose_name="Опубликовать на главной как новость без картинки", default=False)

    class Meta:
        ordering = ['created_date']
        get_latest_by = ['created_date']
        verbose_name = 'Страница'
        verbose_name_plural = "Страницы"