# Generated by Django 2.1.5 on 2019-05-14 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0009_auto_20190514_1200'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='number',
            field=models.SmallIntegerField(blank=True, default=None, null=True, verbose_name='Порядок сортировки'),
        ),
    ]
