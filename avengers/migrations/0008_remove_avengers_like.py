# Generated by Django 3.1.2 on 2020-12-30 12:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('avengers', '0007_auto_20201230_2057'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='avengers',
            name='like',
        ),
    ]
