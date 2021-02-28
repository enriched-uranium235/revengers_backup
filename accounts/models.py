from django.contrib.auth.models import User
from django.db import models
from PIL import Image

# プロフィールクラス
class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name='ユーザー', on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(verbose_name="プロフィール画像", blank=True, null=True, upload_to='images/', default='noimage2.png')

    def __str__(self):
        return f'{self.user.username} Profile'

    @property
    def followers(self):
        return Follow.objects.filter(follow_user=self.user).count()

    @property
    def following(self):
        return Follow.objects.filter(user=self.user).count()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save()

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Follow(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    follow_user = models.ForeignKey(User, related_name='follow_user', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

