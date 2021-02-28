# Generated by Django 3.1.2 on 2021-01-18 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avengers', '0069_favorite_is_favorite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorite',
            name='is_favorite',
            field=models.BooleanField(default=False, verbose_name='お気に入り設定(チェックを入れて更新するとお気に入りとして保存され、チェックを外して更新するとお気に入りの対象から外れます。)'),
        ),
    ]