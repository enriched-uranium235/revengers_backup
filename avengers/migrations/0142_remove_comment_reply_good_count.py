# Generated by Django 3.1.2 on 2021-03-03 07:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('avengers', '0141_view'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='reply_good_count',
        ),
    ]