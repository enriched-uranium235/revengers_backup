# Generated by Django 3.1.2 on 2021-01-21 06:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('avengers', '0083_auto_20210120_1942'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friend',
            name='f_group',
        ),
        migrations.RemoveField(
            model_name='friend',
            name='f_owner',
        ),
        migrations.RemoveField(
            model_name='friend',
            name='f_user',
        ),
        migrations.RemoveField(
            model_name='good',
            name='message',
        ),
        migrations.RemoveField(
            model_name='good',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='message',
            name='m_group',
        ),
        migrations.RemoveField(
            model_name='message',
            name='m_owner',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Friend',
        ),
        migrations.DeleteModel(
            name='Good',
        ),
        migrations.DeleteModel(
            name='Message',
        ),
    ]