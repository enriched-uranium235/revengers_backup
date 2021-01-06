# Generated by Django 3.1.2 on 2021-01-04 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avengers', '0015_delete_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='投稿日時')),
            ],
            options={
                'db_table': 'Message',
            },
        ),
    ]