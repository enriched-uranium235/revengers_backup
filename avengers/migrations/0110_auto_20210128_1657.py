# Generated by Django 3.1.2 on 2021-01-28 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avengers', '0109_delete_blacksubscribe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avengers',
            name='media1',
            field=models.FileField(blank=True, default='Null', null=True, upload_to='', verbose_name='音声'),
        ),
        migrations.AlterField(
            model_name='avengers',
            name='media2',
            field=models.FileField(blank=True, default='Null', null=True, upload_to='', verbose_name='動画'),
        ),
        migrations.AlterField(
            model_name='avengers',
            name='photo1',
            field=models.ImageField(blank=True, default='Null', null=True, upload_to='', verbose_name='写真'),
        ),
    ]