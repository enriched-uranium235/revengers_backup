# Generated by Django 3.1.2 on 2021-01-18 08:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('avengers', '0062_delete_favorite'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('favorite', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='avengers.avengers', verbose_name='対象記事')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]