# Generated by Django 3.1.2 on 2020-12-30 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avengers', '0006_avengers_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avengers',
            name='like',
            field=models.IntegerField(blank=True, default=0, verbose_name='いいね'),
        ),
    ]
