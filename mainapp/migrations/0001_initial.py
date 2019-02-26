# Generated by Django 2.1.5 on 2019-02-26 12:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('url_code', models.CharField(blank=True, default='НЕ УКАЗАН', max_length=30, verbose_name='Код ссылки')),
                ('short_description', models.CharField(blank=True, max_length=200, verbose_name='Краткое описание')),
                ('published_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата публикации')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания')),
                ('publish_on_main_page', models.BooleanField(default=False, verbose_name='Опубликовать на главной')),
                ('publish_on_news_page', models.BooleanField(default=False, verbose_name='Опубликовать в ленте новостей')),
                ('secondery_main', models.BooleanField(default=False, verbose_name='Опубликовать на главной как новость без картинки')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Страница',
                'verbose_name_plural': 'Страницы',
                'ordering': ['created_date'],
                'get_latest_by': ['created_date'],
            },
        ),
    ]