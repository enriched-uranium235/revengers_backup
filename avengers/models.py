from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver


# Avengers被害投稿
class Avengers(models.Model):
    user = models.ForeignKey(User, verbose_name='ユーザー', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='被害内容', max_length=40)
    group = models.CharField(verbose_name='会社名・加害者名・学校名(未記入でも可)', max_length=40, blank=True, null=True)
    content = models.TextField(verbose_name='被害内容詳細(職場いじめ、パワハラ等)', blank=True, null=True)
    photo1 = models.ImageField(verbose_name='写真', blank=True, null=True)
    media1 = models.FileField(verbose_name='音声', blank=True, null=True)
    media2 = models.FileField(verbose_name='動画', blank=True, null=True)
    good_count = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    show = models.BooleanField(verbose_name='被害記事を公開したい場合こちらのチェックボックスにチェックをお願いします。', default=False)
    is_reported = models.CharField(verbose_name='通報状態', max_length=10, default='')
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    class Meta:
        verbose_name_plural = 'Avengers'

    def __str__(self):
        return self.title

    @property
    def number_of_comments(self):
        return Comment.objects.filter(post=self).count()

# コメントクラス
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_owner')
    content = models.TextField(verbose_name='コメント内容', blank=True, null=True)
    post = models.ForeignKey(Avengers, verbose_name='対象記事', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', verbose_name='親コメント', null=True, blank=True, on_delete=models.CASCADE)
    good_count = models.IntegerField(default=0)
    comment_c = models.IntegerField(default=0)
    is_reported = models.CharField('通報状態', max_length=10, default='')
    created_at = models.DateTimeField(verbose_name='投稿日時')

    def __str__(self):
        return self.content + '(' + str(self.user) + ')'

# 運営からのお知らせ
class Notice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='management')
    posted = models.DateTimeField(verbose_name='通知日時', auto_now_add=True)
    title = models.CharField(verbose_name='タイトル', max_length=100)
    content = models.TextField(verbose_name='お知らせ内容')

    def __str__(self):
        return self.content

    @property
    def number_of_reads(self):
        return NoticeRead.objects.filter(notice=self).filter(is_read=True).count()

# お知らせ既読確認
class NoticeRead(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='read_owner')
    notice = models.ForeignKey(Notice, verbose_name='通知', on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)

# コミュニティースレッド
class Post(models.Model):
    content = models.TextField(max_length=300)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    good_count = models.IntegerField(default=0)
    is_reported = models.CharField('通報状態', max_length=10, default='')

    def __str__(self):
        return self.content

    @property
    def number_of_comments(self):
        return Comment2.objects.filter(post_connected=self).count()

# コメント(スレッド用)
class Comment2(models.Model):
    content = models.TextField(max_length=150)
    date_posted = models.DateTimeField(verbose_name='コメント日時')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_connected = models.ForeignKey(Post, on_delete=models.CASCADE)
    good_count = models.IntegerField(default=0)
    is_reported = models.CharField('通報状態', max_length=10, default='')


# スピーチ投稿
class Experiences(models.Model):
    user = models.ForeignKey(User, verbose_name='ユーザー', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='タイトル', max_length=40)
    content = models.TextField(verbose_name='投稿内容説明', blank=True, null=True)
    photo = models.ImageField(verbose_name='動画紹介画像', null=True)
    video = models.FileField(verbose_name='投稿動画', null=True)
    good_count = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(verbose_name='投稿日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    def __str__(self):
        return self.title

    @property
    def number_of_comments(self):
        return Comment3.objects.filter(post_connected=self).count()

# コメント(スピーチ投稿用)
class Comment3(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=150)
    post_connected = models.ForeignKey(Experiences, verbose_name='対象記事', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', verbose_name='親コメント', null=True, blank=True, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(verbose_name='コメント日時')
    good_count = models.IntegerField(default=0)
    comment_c = models.IntegerField(default=0)
    is_reported = models.CharField('通報状態', max_length=10, default='')

    def __str__(self):
        return self.content + '(' + str(self.author) + ')'


# Goodクラス(スレッド用)
class Good(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='good_owner')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return 'good for "' + str(self.post) + '" (by ' + \
               str(self.owner) + ')'

# Good2クラス(Avengersクラス用)
class Good2(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='good_owner2')
    avengers = models.ForeignKey(Avengers, on_delete=models.CASCADE)

    def __str__(self):
        return 'good for "' + str(self.avengers) + '" (by ' + \
               str(self.owner) + ')'

# Good3クラス(コメント用)
class Good3(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='good_owner3')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    def __str__(self):
        return 'good for "' + str(self.comment) + '" (by ' + \
               str(self.owner) + ')'

# Good4クラス(コメント2用)
class Good4(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='good_owner4')
    comment = models.ForeignKey(Comment2, on_delete=models.CASCADE)

    def __str__(self):
        return 'good for "' + str(self.comment) + '" (by ' + \
               str(self.owner) + ')'


# Good5クラス(スピーチ用)
class Good5(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='good_owner5')
    experiences = models.ForeignKey(Experiences, on_delete=models.CASCADE)

    def __str__(self):
        return 'good for "' + str(self.experiences) + '" (by ' + str(self.owner) + ')'


# Good6クラス(コメント3用)
class Good6(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='good_owner6')
    comment = models.ForeignKey(Comment3, on_delete=models.CASCADE)

    def __str__(self):
        return 'good for "' + str(self.comment) + '" (by ' + str(self.owner) + ')'

# お気に入り投稿
class Favorite(models.Model):
    owner = models.ForeignKey(User, verbose_name='ユーザー', on_delete=models.CASCADE, related_name='favorite_owner')
    favorite = models.ForeignKey(Avengers, verbose_name='保存した記事', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='被害内容', max_length=40)
    group = models.CharField(verbose_name='所属団体名・加害者名(未記入でも可)', max_length=40, blank=True, null=True)
    content = models.TextField(verbose_name='被害内容詳細(職場いじめ、パワハラ等)', blank=True, null=True)
    photo1 = models.ImageField(verbose_name='写真', blank=True, null=True)
    media1 = models.FileField(verbose_name='音声', blank=True, null=True)
    media2 = models.FileField(verbose_name='動画', blank=True, null=True)
    number = models.IntegerField(default=0)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    def __str__(self):
        return str(self.owner) + ' (favorite:"' + str(self.favorite) + '")'

# お気に入り投稿(experience)
class Favorite2(models.Model):
    owner = models.ForeignKey(User, verbose_name='ユーザー', on_delete=models.CASCADE, related_name='favorite_owner2')
    favorite = models.ForeignKey(Experiences, verbose_name='保存した記事', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='タイトル', max_length=40)
    content = models.TextField(verbose_name='被害内容詳細(職場いじめ、パワハラ等)', blank=True, null=True)
    photo = models.ImageField(verbose_name='画像', blank=True, null=True)
    video = models.FileField(verbose_name='動画', blank=True, null=True)
    number = models.IntegerField(default=0)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    def __str__(self):
        return str(self.owner) + ' (favorite:"' + str(self.favorite) + '")'

# DMクラス(フォローしたユーザーにダイレクトメッセージを送る)
class DM(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="dm_owner")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="dm_user")
    title = models.CharField(max_length=40, blank=True, null=True)
    content = models.TextField(max_length=250)
    is_read = models.BooleanField(default=False)
    is_reported = models.CharField('通報状態', max_length=10, default='')
    dm_created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content + str(self.owner) + " が " + str(self.user) + " にDM " + str(self.dm_created_at)

    class Meta:
        ordering = ["-dm_created_at"]

# 通報機能(Avengers投稿)
class Report(models.Model):
    user = models.CharField(verbose_name='投稿主', max_length=40)
    user_id = models.IntegerField(verbose_name='id', default=0)
    report = models.ForeignKey(Avengers, verbose_name='通報された投稿', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='被害内容', max_length=40)
    group = models.CharField(verbose_name='企業名・加害者名', max_length=40, blank=True, null=True)
    content = models.TextField(verbose_name='詳細', blank=True, null=True)
    photo1 = models.ImageField(verbose_name='写真', blank=True, null=True)
    media1 = models.FileField(verbose_name='音声', blank=True, null=True)
    media2 = models.FileField(verbose_name='動画', blank=True, null=True)
    number = models.IntegerField(default=0)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    reported_date = models.DateTimeField(verbose_name='通報日時', auto_now=True)

    def __str__(self):
        return self.title

# 通報機能(Comment,Reply用)
class Report2(models.Model):
    user = models.CharField(verbose_name='コメント主', max_length=40)
    user_id = models.IntegerField(verbose_name='id', default=0)
    report = models.ForeignKey(Comment, verbose_name='通報されたコメント', on_delete=models.CASCADE)
    content = models.TextField(verbose_name='コメント内容', blank=True, null=True)
    number1 = models.IntegerField(verbose_name='投稿id', default=0)
    number2 = models.IntegerField(verbose_name='コメントid', default=0)
    created_at = models.DateTimeField(verbose_name='通報日時', auto_now=True)

    def __str__(self):
        return self.content

# 通報機能(Post用)
class Report3(models.Model):
    user = models.CharField(verbose_name='スレッド主', max_length=40)
    user_id = models.IntegerField(verbose_name='id', default=0)
    report = models.ForeignKey(Post, verbose_name='通報されたスレッド', on_delete=models.CASCADE)
    content = models.TextField(verbose_name='スレッド内容', blank=True, null=True)
    number = models.IntegerField(verbose_name='スレッドid', default=0)
    created_at = models.DateTimeField(verbose_name='通報日時', auto_now=True)

    def __str__(self):
        return self.content

# 通報機能(DM用)
class Report4(models.Model):
    user = models.CharField(verbose_name='メッセージ送信者', max_length=40)
    user_id = models.IntegerField(verbose_name='id', default=0)
    report = models.ForeignKey(DM, verbose_name='通報されたDM', on_delete=models.CASCADE)
    content = models.TextField(verbose_name='DM内容', blank=True, null=True)
    number = models.IntegerField(verbose_name='DMid', default=0)
    created_at = models.DateTimeField(verbose_name='通報日時', auto_now=True)

# 通報機能(スレッド投稿)
class Report5(models.Model):
    user = models.CharField(verbose_name='コメントユーザー', max_length=40)
    user_id = models.IntegerField(verbose_name='id', default=0)
    report = models.ForeignKey(Comment2, verbose_name='通報されたコメント', on_delete=models.CASCADE)
    content = models.TextField(verbose_name='コメント内容', blank=True, null=True)
    number = models.IntegerField(verbose_name='コメントID', default=0)
    created_at = models.DateTimeField(verbose_name='通報日時', auto_now=True)

# 通報機能(スピーチ投稿)
class Report6(models.Model):
    user = models.CharField(verbose_name='スピーチ投稿者', max_length=40)
    user_id = models.IntegerField(verbose_name='id', default=0)
    report = models.ForeignKey(Experiences, verbose_name='通報されたスピーチ', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='タイトル', max_length=40)
    content = models.TextField(verbose_name='説明文', blank=True, null=True)
    photo = models.ImageField(verbose_name='紹介画像', blank=True, null=True)
    video = models.FileField(verbose_name='スピーチ動画')
    number = models.IntegerField(default=0)
    created_at = models.DateTimeField(verbose_name='通報日時', auto_now=True)

# 通報機能(Comment3)
class Report7(models.Model):
    user = models.CharField(verbose_name='コメントユーザー', max_length=40)
    user_id = models.IntegerField(verbose_name='id', default=0)
    report = models.ForeignKey(Comment3, verbose_name='通報されたコメント', on_delete=models.CASCADE)
    content = models.TextField(verbose_name='コメント内容', blank=True, null=True)
    number = models.IntegerField(verbose_name='コメントID', default=0)
    created_at = models.DateTimeField(verbose_name='通報日時', auto_now=True)

# 通報機能(Avengers投稿永久保存用)
class Report1_1(models.Model):
    user = models.CharField(verbose_name='投稿主', max_length=40)
    user_id = models.IntegerField(verbose_name='id', default=0)
    title = models.CharField(verbose_name='被害内容', max_length=40)
    group = models.CharField(verbose_name='企業名・加害者名', max_length=40, blank=True, null=True)
    content = models.TextField(verbose_name='詳細', blank=True, null=True)
    photo1 = models.ImageField(verbose_name='写真', blank=True, null=True)
    media1 = models.FileField(verbose_name='音声', blank=True, null=True)
    media2 = models.FileField(verbose_name='動画', blank=True, null=True)
    number = models.IntegerField(default=0)
    created_at = models.CharField(verbose_name='作成日時', max_length=40, blank=True, null=True)
    reported_date = models.CharField(verbose_name='通報日時', max_length=40, blank=True, null=True)
    owner = models.CharField(verbose_name='通報者', max_length=40, default='No name')
    owner_id = models.IntegerField(verbose_name='通報者ID', default=0)

    def __str__(self):
        return self.title

# 通報機能(Comment,Reply永久保存用)
class Report2_1(models.Model):
    user = models.CharField(verbose_name='コメント主', max_length=40)
    user_id = models.IntegerField(verbose_name='id', default=0)
    content = models.TextField(verbose_name='コメント内容', blank=True, null=True)
    number1 = models.IntegerField(verbose_name='投稿id', default=0)
    number2 = models.IntegerField(verbose_name='コメントid', default=0)
    created_at = models.CharField(verbose_name='投稿日時', max_length=40, blank=True, null=True)
    reported_at = models.CharField(verbose_name='通報日時', max_length=40, blank=True, null=True)
    owner = models.CharField(verbose_name='通報者', max_length=40, default='No name')
    owner_id = models.IntegerField(verbose_name='通報者ID', default=0)

    def __str__(self):
        return self.content

# 通報機能(Post永久保存用)
class Report3_1(models.Model):
    user = models.CharField(verbose_name='スレッド主', max_length=40)
    user_id = models.IntegerField(verbose_name='id', default=0)
    content = models.TextField(verbose_name='スレッド内容', blank=True, null=True)
    number = models.IntegerField(verbose_name='スレッドid', default=0)
    created_at = models.CharField(verbose_name='投稿日時', max_length=40, blank=True, null=True)
    reported_at = models.CharField(verbose_name='通報日時', max_length=40, blank=True, null=True)
    owner = models.CharField(verbose_name='通報者', max_length=40, default='No name')
    owner_id = models.IntegerField(verbose_name='通報者ID', default=0)

    def __str__(self):
        return self.content

# 通報機能(DM永久保存用)
class Report4_1(models.Model):
    user = models.CharField(verbose_name='メッセージ送信者', max_length=40)
    user_id = models.IntegerField(verbose_name='id', default=0)
    content = models.TextField(verbose_name='DM内容', blank=True, null=True)
    number = models.IntegerField(verbose_name='DMid', default=0)
    created_at = models.CharField(verbose_name='投稿日時', max_length=40, blank=True, null=True)
    reported_at = models.CharField(verbose_name='通報日時', max_length=40, blank=True, null=True)
    owner = models.CharField(verbose_name='通報者', max_length=40, default='No name')
    owner_id = models.IntegerField(verbose_name='通報者ID', default=0)

# 通報機能(スレッド投稿永久保存)
class Report5_1(models.Model):
    user = models.CharField(verbose_name='コメントユーザー', max_length=40)
    user_id = models.IntegerField(verbose_name='id', default=0)
    report = models.ForeignKey(Comment2, verbose_name='通報されたコメント', on_delete=models.CASCADE)
    content = models.TextField(verbose_name='コメント内容', blank=True, null=True)
    number = models.IntegerField(verbose_name='コメントID', default=0)
    created_at = models.DateTimeField(verbose_name='投稿日時')
    reported_at = models.DateTimeField(verbose_name='通報日時')
    owner = models.CharField(verbose_name='通報者', max_length=40)
    owner_id = models.IntegerField(verbose_name='通報者ID', default=0)

# 通報機能(スピーチ投稿永久保存)
class Report6_1(models.Model):
    user = models.CharField(verbose_name='スピーチ投稿者', max_length=40)
    user_id = models.IntegerField(verbose_name='id', default=0)
    report = models.ForeignKey(Experiences, verbose_name='通報されたスピーチ', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='タイトル', max_length=40)
    content = models.TextField(verbose_name='説明文', blank=True, null=True)
    photo = models.ImageField(verbose_name='紹介画像', blank=True, null=True)
    video = models.FileField(verbose_name='スピーチ動画')
    number = models.IntegerField(default=0)
    created_at = models.DateTimeField(verbose_name='投稿日時', auto_now=True)
    reported_at = models.DateTimeField(verbose_name='通報日時')
    owner = models.CharField(verbose_name='通報者', max_length=40)
    owner_id = models.IntegerField(verbose_name='通報者ID', default=0)


# 通報機能(Comment3永久保存)
class Report7_1(models.Model):
    user = models.CharField(verbose_name='コメントユーザー', max_length=40)
    user_id = models.IntegerField(verbose_name='id', default=0)
    report = models.ForeignKey(Comment3, verbose_name='通報されたコメント', on_delete=models.CASCADE)
    content = models.TextField(verbose_name='コメント内容', blank=True, null=True)
    number = models.IntegerField(verbose_name='コメントID', default=0)
    created_at = models.DateTimeField(verbose_name='投稿日時', auto_now=True)
    reported_at = models.DateTimeField(verbose_name='通報日時')
    owner = models.CharField(verbose_name='通報者', max_length=40)
    owner_id = models.IntegerField(verbose_name='通報者ID', default=0)


# ブラックリストクラス(各ユーザーごとに通報された回数を取得してデータ集計するためのもの)
class BlackList(models.Model):
    user = models.ForeignKey(User, verbose_name='ユーザー', on_delete=models.CASCADE, related_name='blacklist')
    is_reported = models.IntegerField(verbose_name='通報された回数', default=0)

    def get_blacklist_count(self):
        return BlackList.objects.all().count()

# ブラックリストクラス(削除済みユーザーを含む全て)
class AllBlackList(models.Model):
    user = models.CharField(verbose_name='ユーザー', max_length=40)
    user_id = models.IntegerField(verbose_name='ユーザーID', default=0)
    is_reported = models.IntegerField(verbose_name='通報された回数', default=0)

# ログクラス(各ユーザーごとに閲覧履歴を残す)
class AvengersLog(models.Model):
    user = models.ForeignKey(User, verbose_name='ユーザー', on_delete=models.CASCADE)
    avengers = models.ForeignKey(Avengers, verbose_name='履歴に記録される投稿', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='被害内容', max_length=40)
    group = models.CharField(verbose_name='所属団体名・加害者名(未記入でも可)', max_length=40, blank=True, null=True)
    content = models.TextField(verbose_name='被害内容詳細(職場いじめ、パワハラ等)', blank=True, null=True)
    photo1 = models.ImageField(verbose_name='写真', blank=True, null=True)
    media1 = models.FileField(verbose_name='音声', blank=True, null=True)
    media2 = models.FileField(verbose_name='動画', blank=True, null=True)
    number = models.IntegerField(verbose_name='整理番号', default=0)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)

    class Meta:
        verbose_name_plural = 'AvengersLog'

    def __str__(self):
        return self.title

# ログクラス(各ユーザーごとに閲覧履歴を残す(experience))
class ExperiencesLog(models.Model):
    user = models.ForeignKey(User, verbose_name='ユーザー', on_delete=models.CASCADE)
    avengers = models.ForeignKey(Experiences, verbose_name='履歴に記録される投稿', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='被害内容', max_length=40)
    content = models.TextField(verbose_name='被害内容詳細(職場いじめ、パワハラ等)', blank=True, null=True)
    photo = models.ImageField(verbose_name='写真', blank=True, null=True)
    video = models.FileField(verbose_name='動画', blank=True, null=True)
    number = models.IntegerField(verbose_name='整理番号', default=0)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)

    class Meta:
        verbose_name_plural = 'ExperiencesLog'

    def __str__(self):
        return self.title


# ログイン・ログアウトの履歴を管理
class AttendanceRecord(models.Model):
    """ログイン・ログアウトの履歴"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='ユーザー', on_delete=models.CASCADE)
    login_time = models.DateTimeField('ログイン時刻', blank=True, null=True)
    logout_time = models.DateTimeField('ログアウト時刻', blank=True, null=True)

    def __str__(self):
        login_dt = timezone.localtime(self.login_time)
        return '{0} - {1.year}/{1.month}/{1.day} {1.hour}:{1.minute}:{1.second} - {2}'.format(
            self.user.username, login_dt, self.get_diff_time()
        )

    def get_diff_time(self):
        """ログアウト時間ーログイン時間"""
        if not self.logout_time:
            return 'ログアウトしていません'
        else:
            td = self.logout_time - self.login_time
            return '{0}時間{1}分'.format(
                td.seconds // 3600, (td.seconds // 60) % 60)

# 全てのログを作成・保存
class AttendanceAllRecord(models.Model):
    """ログイン・ログアウトの履歴(削除済みユーザーを含む)"""

    user = models.CharField(verbose_name='ユーザー名', max_length=40)
    user_id = models.IntegerField(default=0)
    user_email = models.TextField(verbose_name='アドレス', blank=True, null=True)
    login_time = models.CharField('ログイン時刻', max_length=40, blank=True, null=True)
    logout_time = models.CharField('ログアウト時刻', max_length=40, blank=True, null=True)

    def __str__(self):
        login_dt = timezone.localtime(self.login_time)
        return '{0} - {1.year}/{1.month}/{1.day} {1.hour}:{1.minute}:{1.second} - {2}'.format(
            self.user, login_dt, self.get_diff_time()
        )

    def get_diff_time(self):
        """ログアウト時間ーログイン時間"""
        if not self.logout_time:
            return 'ログアウトしていません'
        else:
            td = self.logout_time - self.login_time
            return '{0}時間{1}分'.format(
                td.seconds // 3600, (td.seconds // 60) % 60)


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    """ログインした際に呼ばれる"""
    AttendanceRecord.objects.create(user=user, login_time=timezone.now())
    AttendanceAllRecord.objects.create(user=user.username, user_id=user.id, user_email=user.email, login_time=str(timezone.now()))


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    """ログアウトした際に呼ばれる"""
    records = AttendanceRecord.objects.filter(user=user, logout_time__isnull=True)
    if records:
        record = records.latest('pk')
        record.logout_time = timezone.now()
        record.save()

    records2 = AttendanceAllRecord.objects.filter(user=user, logout_time__isnull=True)
    if records2:
        records2 = records2.latest('pk')
        records2.logout_time = str(timezone.now())
        records2.save()