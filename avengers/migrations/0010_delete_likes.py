# Generated by Django 3.1.2 on 2020-12-30 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('avengers', '0009_likes'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Likes',
        ),
    ]