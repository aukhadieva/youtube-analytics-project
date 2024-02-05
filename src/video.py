import os

from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()


class Video:
    """Класс для видео."""

    api_key: str = os.getenv('YT_API_KEY')

    def __init__(self, video_id):
        """Экземпляр инициализируется id видео. Дальше все данные будут подтягиваться по API."""
        self.video_id = video_id
        self.video_response = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                               id=video_id).execute()
        self.video_title: str = self.video_response['items'][0]['snippet']['title']
        self.url: str = f'https://www.youtube.com/watch?v={self.video_id}'
        self.view_count: int = self.video_response['items'][0]['statistics']['viewCount']
        self.like_count: int = self.video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        """Возвращает строковое представление объекта в виде названия видео."""
        return self.video_title

    @classmethod
    def get_service(cls):
        """Класс-метод, возвращающий объект для работы с YouTube API."""
        youtube = build('youtube', 'v3', developerKey=cls.api_key)
        return youtube


class PLVideo(Video):
    """Класс для плейлиста."""

    def __init__(self, video_id, playlist_id):
        """
        Расширяет функционал класса Video.
        Добавляет дополнительные атрибуты, содержащие id плейлиста
        и id видеороликов из плейлиста.
        """
        super().__init__(video_id)
        self.playlist_id = playlist_id
        self.playlist_videos = self.get_service().playlistItems().list(playlistId=self.playlist_id,
                                                                       part='contentDetails',
                                                                       maxResults=50, ).execute()
