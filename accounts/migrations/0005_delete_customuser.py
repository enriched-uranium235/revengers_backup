# Generated by Django 3.1.2 on 2021-01-23 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20210123_1757'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]