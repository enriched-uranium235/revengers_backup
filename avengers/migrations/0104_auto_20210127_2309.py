# Generated by Django 3.1.2 on 2021-01-27 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avengers', '0103_report3_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='user_id',
            field=models.IntegerField(default=0, verbose_name='id'),
        ),
        migrations.AddField(
            model_name='report2',
            name='user_id',
            field=models.IntegerField(default=0, verbose_name='id'),
        ),
        migrations.AddField(
            model_name='report3',
            name='user_id',
            field=models.IntegerField(default=0, verbose_name='id'),
        ),
    ]