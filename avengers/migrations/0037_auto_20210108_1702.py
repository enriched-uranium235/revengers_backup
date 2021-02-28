# Generated by Django 3.1.2 on 2021-01-08 08:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('avengers', '0036_auto_20210108_1519'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='プロフィール画像')),
                ('content', models.TextField(blank=True, null=True, verbose_name='自己紹介文')),
                ('place', models.CharField(blank=True, max_length=40, null=True, verbose_name='居住地')),
                ('hobby', models.TextField(blank=True, null=True, verbose_name='趣味')),
                ('show', models.BooleanField(default=False, verbose_name='公開非公開')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='ユーザー')),
            ],
        ),
        migrations.DeleteModel(
            name='Avator',
        ),
    ]