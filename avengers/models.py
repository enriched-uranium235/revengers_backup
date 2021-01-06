from accounts.models import CustomUser
from django.db import models
from django.utils import timezone

class Avengers(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.PROTECT)
    title = models.CharField(verbose_name='タイトル', max_length=40)
    group = models.CharField(verbose_name='所属団体名(未記入でも可)', max_length=40, blank=True, null=True)
    content = models.TextField(verbose_name='被害内容詳細(職場いじめ、パワハラ等)', blank=True, null=True)
    photo1 = models.ImageField(verbose_name='写真1', blank=True, null=True)
    photo2 = models.ImageField(verbose_name='写真2', blank=True, null=True)
    photo3 = models.ImageField(verbose_name='写真3', blank=True, null=True)
    media1 = models.FileField(verbose_name='音声1', blank=True, null=True)
    media2 = models.FileField(verbose_name='音声2', blank=True, null=True)
    media3 = models.FileField(verbose_name='音声3', blank=True, null=True)
    media4 = models.FileField(verbose_name='動画1', blank=True, null=True)
    media5 = models.FileField(verbose_name='動画2', blank=True, null=True)
    media6 = models.FileField(verbose_name='動画3', blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    class Meta:
        verbose_name_plural = 'Avengers'

    def __str__(self):
        return self.title

class Message(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.PROTECT)
    content = models.TextField(verbose_name="投稿コメント", blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='投稿日時', auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Message'

    def __str__(self):
        return self.content

class Comment(models.Model):
    content = models.TextField(verbose_name='コメント内容', blank=True, null=True)
    post = models.ForeignKey(Avengers, verbose_name='対象記事', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', verbose_name='親コメント', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.content