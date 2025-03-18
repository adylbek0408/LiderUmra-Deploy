import logging
from datetime import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from apps.blog.models import YouTubeChannelSettings, Lesson

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Синхронизирует видео с YouTube канала и создает новые уроки'

    def handle(self, *args, **options):
        self.stdout.write('Начинаем синхронизацию с YouTube...')

        channels = YouTubeChannelSettings.objects.filter(auto_import=True)

        for channel in channels:
            try:
                self.stdout.write(f'Обработка канала: {channel.channel_id}')

                youtube = build('youtube', 'v3', developerKey=channel.api_key)

                # Получение последних видео
                request = youtube.search().list(
                    part='snippet',
                    channelId=channel.channel_id,
                    order='date',
                    type='video',
                    maxResults=10
                )

                response = request.execute()

                new_videos_count = 0
                for item in response.get('items', []):
                    video_id = item['id']['videoId']
                    title = item['snippet']['title']
                    description = item['snippet']['description']
                    published_at = item['snippet']['publishedAt']

                    # Проверка существования видео
                    if not Lesson.objects.filter(youtube_id=video_id).exists():
                        # Получение расширенной информации о видео
                        video_request = youtube.videos().list(
                            part='snippet,contentDetails',
                            id=video_id
                        )
                        video_response = video_request.execute()

                        if video_response['items']:
                            video_info = video_response['items'][0]
                            full_description = video_info['snippet']['description']

                            # Создаем новый урок
                            lesson = Lesson(
                                title=title,
                                rich=full_description,
                                video_url=f"https://www.youtube.com/watch?v={video_id}",
                                youtube_id=video_id,
                                created_at=datetime.strptime(published_at, '%Y-%m-%dT%H:%M:%SZ').replace(
                                    tzinfo=timezone.utc)
                            )
                            lesson.save()
                            new_videos_count += 1

                # Обновляем время последней синхронизации
                channel.last_sync = timezone.now()
                channel.save()

                self.stdout.write(self.style.SUCCESS(f'Добавлено {new_videos_count} новых видео'))

            except HttpError as e:
                self.stdout.write(self.style.ERROR(f"Ошибка YouTube API: {str(e)}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Непредвиденная ошибка: {str(e)}"))

        self.stdout.write(self.style.SUCCESS('Синхронизация завершена.'))