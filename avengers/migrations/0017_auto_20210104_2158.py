# Generated by Django 3.1.2 on 2021-01-04 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avengers', '0016_message'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Message',
        ),
        migrations.AddField(
            model_name='avengers',
            name='content2',
            field=models.TextField(blank=True, null=True, verbose_name='コメント内容'),
        ),
    ]