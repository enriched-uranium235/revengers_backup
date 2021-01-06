import csv
import datetime
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from ...models import Avengers

class Command(BaseCommand):
    help = "Backup Diary data"

    def handle(self, *args, **options):
        # 実行時のYYYYMMDDを取得
        date = datetime.date.today().strftime("%Y%m%d")

        # 保存ファイルの相対パス
        file_path = settings.BACKUP_PATH + 'diary_' + date + '.csv'

        # 保存ディレクトリが存在しなければ作成
        os.makedirs(settings.BACKUP_PATH, exist_ok=True)

        # バックアップファイルの作成
        with open (file_path, 'w') as file:
            writer = csv.writer(file)

            # ヘッダーへの書き込み
            header = [field.name for field in Avengers._meta.fields]
            writer.writerow(header)

            # Avengersテーブルの全データを取得
            diaries = Avengers.objects.all()

            # データ部分の書き込み
            for items in diaries:
                writer.writerow([str(items.user),
                                 items.title,
                                 items.content,
                                 str(items.photo1),
                                 str(items.photo2),
                                 str(items.photo3),
                                 str(items.media1),
                                 str(items.media2),
                                 str(items.media3),
                                 str(items.media4),
                                 str(items.media5),
                                 str(items.media6),
                                 str(items.created_at),
                                 str(items.updated_at)])

            # 保存ディレクトリのファイルリストを取得
            files = os.listdir(settings.BACKUP_PATH)
            # ファイルが設定数以上あったら一番古いファイルを削除
            if len(files) >= settings.NUM_SAVED_BACKUP:
                files.sort()
                os.remove(settings.BACKUP_PATH + files[0])