# Generated by Django 3.1.2 on 2021-02-09 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avengers', '0129_auto_20210209_2127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment2',
            name='date_posted',
            field=models.DateTimeField(auto_now=True),
        ),
    ]