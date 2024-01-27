import json
import os

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        channel = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.title: str = channel['items'][0]['snippet']['title']
        self.video_count: str = channel["items"][0]["statistics"]["videoCount"]
        self.url: str = channel['items'][0]['snippet']['thumbnails']['default']['url']
        self.description: str = channel['items'][0]['snippet']['description']
        self.subscriber_count: str = channel["items"][0]["statistics"]['subscriberCount']
        self.view_count: str = channel["items"][0]["statistics"]['viewCount']

    @property
    def channel_id(self):
        return self.__channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """Класс-метод, возвращающий объект для работы с YouTube API."""
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def to_json(self, json_file):
        """Сохраняет в файл значения атрибутов экземпляра `Channel`."""
        state = {"channel_id": self.__channel_id, "title": self.title, "description": self.description, "url": self.url,
                 "subscriber_count": self.subscriber_count, "video_count": self.video_count,
                 "view_count": self.view_count}
        with open(json_file, 'w', encoding='utf-8') as outfile:
            json.dump(state, outfile, indent=4)
