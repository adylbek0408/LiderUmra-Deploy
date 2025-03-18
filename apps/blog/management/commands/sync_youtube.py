import logging
from datetime import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from apps.blog.models import YouTubeChannelSettings, Lesson
import pytz

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Синхронизирует видео из плейлиста YouTube и создает новые уроки'

    def handle(self, *args, **options):
        self.stdout.write('Начинаем синхронизацию с YouTube...')
        
        channels = YouTubeChannelSettings.objects.filter(auto_import=True)
        
        for channel in channels:
            try:
                self.stdout.write(f'Обработка канала: {channel.channel_id}')
                
                youtube = build('youtube', 'v3', developerKey=channel.api_key)
                
                # ID плейлиста "Лидер Умра"
                # Замените на реальный ID плейлиста
                playlist_id = "PLS9yNEGpQL2mMwAdTALIAeirFu7UB9jhz"  # Например, PL1234567890abcdef
                
                # Получение видео из плейлиста
                request = youtube.playlistItems().list(
                    part='snippet',
                    playlistId=playlist_id,
                    maxResults=50  # максимум 50 видео за один запрос
                )
                
                response = request.execute()
                
                new_videos_count = 0
                for item in response.get('items', []):
                    try:
                        snippet = item['snippet']
                        video_id = snippet['resourceId']['videoId']
                        title = snippet['title']
                        description = snippet.get('description', '')
                        published_at = snippet['publishedAt']
                        
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
                                    created_at=datetime.strptime(published_at, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.UTC)
                                )
                                lesson.save()
                                new_videos_count += 1
                                self.stdout.write(f"Добавлено видео: {title}")
                    except Exception as e:
                        self.stdout.write(f"Ошибка при обработке видео: {str(e)}")
                        continue
                
                # Пагинация - обработка остальных видео, если их больше 50
                while 'nextPageToken' in response:
                    next_page_token = response['nextPageToken']
                    request = youtube.playlistItems().list(
                        part='snippet',
                        playlistId=playlist_id,
                        maxResults=50,
                        pageToken=next_page_token
                    )
                    response = request.execute()
                    
                    for item in response.get('items', []):
                        try:
                            snippet = item['snippet']
                            video_id = snippet['resourceId']['videoId']
                            title = snippet['title']
                            description = snippet.get('description', '')
                            published_at = snippet['publishedAt']
                            
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
                                        created_at=datetime.strptime(published_at, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.UTC)
                                    )
                                    lesson.save()
                                    new_videos_count += 1
                                    self.stdout.write(f"Добавлено видео: {title}")
                        except Exception as e:
                            self.stdout.write(f"Ошибка при обработке видео: {str(e)}")
                            continue
                
                # Обновляем время последней синхронизации
                channel.last_sync = timezone.now()
                channel.save()
                
                self.stdout.write(self.style.SUCCESS(f'Добавлено {new_videos_count} новых видео'))
                
            except HttpError as e:
                self.stdout.write(self.style.ERROR(f"Ошибка YouTube API: {str(e)}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Непредвиденная ошибка: {str(e)}"))
        
        self.stdout.write(self.style.SUCCESS('Синхронизация завершена.'))
