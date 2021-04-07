# Generated by Django 3.1.2 on 2021-04-07 11:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('avengers', '0005_auto_20210407_2000'),
    ]

    operations = [
        migrations.CreateModel(
            name='NoticeRead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_read', models.BooleanField(default=False)),
                ('number', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='read_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posted', models.DateTimeField(auto_now_add=True, verbose_name='通知日時')),
                ('title', models.CharField(max_length=100, verbose_name='タイトル')),
                ('content', models.TextField(verbose_name='お知らせ内容')),
                ('read_list', django_mysql.models.ListCharField(models.CharField(max_length=40), max_length=80, size=1)),
                ('read_list2', django_mysql.models.ListCharField(models.CharField(max_length=40), max_length=80, size=1)),
                ('read_list3', django_mysql.models.ListCharField(models.CharField(max_length=40), max_length=80, size=1)),
                ('read_list4', django_mysql.models.ListCharField(models.CharField(max_length=40), max_length=80, size=1)),
                ('read_list5', django_mysql.models.ListCharField(models.CharField(max_length=40), max_length=80, size=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='management', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]