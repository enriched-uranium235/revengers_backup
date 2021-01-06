# Generated by Django 3.1.2 on 2020-12-28 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avengers', '0002_auto_20201228_1656'),
    ]

    operations = [
        migrations.AddField(
            model_name='avengers',
            name='media4',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='動画1'),
        ),
        migrations.AddField(
            model_name='avengers',
            name='media5',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='動画2'),
        ),
        migrations.AddField(
            model_name='avengers',
            name='media6',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='動画3'),
        ),
        migrations.AlterField(
            model_name='avengers',
            name='media1',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='音声1'),
        ),
        migrations.AlterField(
            model_name='avengers',
            name='media2',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='音声2'),
        ),
        migrations.AlterField(
            model_name='avengers',
            name='media3',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='音声3'),
        ),
    ]