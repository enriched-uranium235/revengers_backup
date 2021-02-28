# Generated by Django 3.1.2 on 2021-01-28 11:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('avengers', '0111_auto_20210128_1702'),
    ]

    operations = [
        migrations.CreateModel(
            name='AvengersLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40, verbose_name='被害内容')),
                ('group', models.CharField(blank=True, max_length=40, null=True, verbose_name='所属団体名・加害者名(未記入でも可)')),
                ('content', models.TextField(blank=True, null=True, verbose_name='被害内容詳細(職場いじめ、パワハラ等)')),
                ('photo1', models.ImageField(blank=True, null=True, upload_to='', verbose_name='写真')),
                ('media1', models.FileField(blank=True, null=True, upload_to='', verbose_name='音声')),
                ('media2', models.FileField(blank=True, null=True, upload_to='', verbose_name='動画')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('avengers', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='avengers.avengers', verbose_name='履歴に記録される投稿')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ユーザー')),
            ],
            options={
                'verbose_name_plural': 'AvengersLog',
            },
        ),
    ]