# Generated by Django 2.1.5 on 2019-04-24 08:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_document_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterField(
            model_name='document',
            name='category',
            field=models.ForeignKey(blank=True, default=None, help_text='\n                                           Используйте это поле для категорий раздела документы:<br>\n                                           В раздел аттестации персонала: категория ВВР-2ГАЦ,<br>\n                                           В раздел спецподготовки: категория ВВР-3ЦСП,<br>\n                                           В раздел аттестации сварочного оборудования: категория АЦСО-46,<br>\n                                           В раздел аттестации сварочных технология: категория АЦСТ-33\n                                           ', null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainapp.Category'),
        ),
    ]