# Generated by Django 3.1.2 on 2021-04-04 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avengers', '0165_avengers_show'),
    ]

    operations = [
        migrations.AddField(
            model_name='dm',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]