import json
import os

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id

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

    @property
    def title(self):
        channel = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        title: str = channel['items'][0]['snippet']['title']
        return title

    @property
    def video_count(self):
        channel = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        video_count: str = channel["items"][0]["statistics"]["videoCount"]
        return video_count

    @property
    def url(self):
        channel = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        url: str = channel['items'][0]['snippet']['thumbnails']['default']['url']
        return url

    @property
    def description(self):
        channel = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        description: str = channel['items'][0]['snippet']['description']
        return description

    @property
    def subscriber_count(self):
        channel = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        subscriber_count: str = channel["items"][0]["statistics"]['subscriberCount']
        return subscriber_count

    @property
    def view_count(self):
        channel = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        view_count: str = channel["items"][0]["statistics"]['viewCount']
        return view_count

    def to_json(self, json_file):
        """Сохраняет в файл значения атрибутов экземпляра `Channel`."""
        state = {"channel_id": self.__channel_id, "title": self.title, "description": self.description, "url": self.url,
                 "subscriber_count": self.subscriber_count, "video_count": self.video_count,
                 "view_count": self.view_count}
        with open(json_file, 'w', encoding='utf-8') as outfile:
            json.dump(state, outfile, indent=4)
