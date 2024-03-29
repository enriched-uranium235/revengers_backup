# Generated by Django 3.1.2 on 2021-04-09 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avengers', '0003_auto_20210408_1800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avengers',
            name='relate',
            field=models.ManyToManyField(blank=True, related_name='_avengers_relate_+', to='avengers.Avengers', verbose_name='関連記事(関連記事の登録は各自で設定お願い致します。複数選択はPCでCTRLキーを押しながらのやり方でしかできません。ご了承ください。)'),
        ),
        migrations.AlterField(
            model_name='avengers',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='tag', to='avengers.Tag', verbose_name='タグ(タグの登録は各自で設定お願い致します。複数選択はPCでCTRLキーを押しながらのやり方でしかできません。ご了承ください。)'),
        ),
        migrations.AlterField(
            model_name='experiences',
            name='relate',
            field=models.ManyToManyField(blank=True, related_name='_experiences_relate_+', to='avengers.Experiences', verbose_name='関連(関連記事の登録は各自で設定お願い致します。複数選択はPCでCTRLキーを押しながらのやり方でしかできません。ご了承ください。)'),
        ),
        migrations.AlterField(
            model_name='experiences',
            name='tag',
            field=models.ManyToManyField(blank=True, related_name='tag', to='avengers.Tag2', verbose_name='タグ(タグの登録は各自で設定お願い致します。複数選択はPCでCTRLキーを押しながらのやり方でしかできません。ご了承ください。)'),
        ),
        migrations.AlterField(
            model_name='post',
            name='tag',
            field=models.ManyToManyField(blank=True, related_name='tag', to='avengers.Tag3', verbose_name='タグ(タグの登録は各自で設定お願い致します。複数選択はPCでCTRLキーを押しながらのやり方でしかできません。ご了承ください。)'),
        ),
    ]
