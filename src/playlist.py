import datetime
import os

import isodate
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()


class PlayList:
    """Класс для плейлиста."""

    api_key: str = os.getenv('YT_API_KEY')

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.playlist_info = self.get_service().playlists().list(id=self.playlist_id, part='contentDetails, '
                                                                                           'snippet').execute()
        self.playlist_videos = self.get_service().playlistItems().list(playlistId=self.playlist_id,
                                                                       part='id,contentDetails,snippet',
                                                                       maxResults=50).execute()
        self.title = self.playlist_info['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'
        self.videoId = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        self.video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                                               id=','.join(self.videoId)).execute()

    @classmethod
    def get_service(cls):
        """Класс-метод, возвращающий объект для работы с YouTube API."""
        youtube = build('youtube', 'v3', developerKey=cls.api_key)
        return youtube

    @property
    def total_duration(self):
        """Возвращает объект класса 'datetime.timedelta',
        С суммарной длительность плейлиста."""
        duration_list = []
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            duration_list.append(duration)
        total_duration = sum(duration_list, datetime.timedelta())
        return total_duration

    def show_best_video(self):
        """Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)."""
        count_like_list = []
        resp_list = []
        for v_id in self.videoId:
            response = self.get_service().videos().list(
                part='snippet,statistics,contentDetails', id=v_id).execute()
            count_like_list.append(response['items'][0]['statistics']['likeCount'])
            resp_list.append(response['items'])
        max_value = max(count_like_list)
        max_index = count_like_list.index(max_value)
        best_video = resp_list[max_index]
        return f'https://youtu.be/{best_video[0]['id']}'
