# Generated by Django 3.1.2 on 2021-03-29 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avengers', '0153_comment3_comment_c'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment3',
            name='comment_c',
        ),
        migrations.AddField(
            model_name='experiences',
            name='comment_c',
            field=models.IntegerField(default=0),
        ),
    ]