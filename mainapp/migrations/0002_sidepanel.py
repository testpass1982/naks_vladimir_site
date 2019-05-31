# Generated by Django 2.1.5 on 2019-05-31 11:52

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SidePanel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('text', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Текст')),
            ],
            options={
                'verbose_name_plural': 'Боковые панели',
                'verbose_name': 'Боковая панель',
            },
        ),
    ]