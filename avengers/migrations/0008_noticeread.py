# Generated by Django 3.1.2 on 2021-04-07 11:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('avengers', '0007_delete_noticeread'),
    ]

    operations = [
        migrations.CreateModel(
            name='NoticeRead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_read', models.BooleanField(default=False)),
                ('number', models.IntegerField(default=0)),
                ('notice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notice', to='avengers.notice')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='read_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]