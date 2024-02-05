import json
import os

from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()


class Channel:
    """Класс для ютуб-канала"""

    api_key: str = os.getenv('YT_API_KEY')

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.title: str = self.channel['items'][0]['snippet']['title']
        self.video_count: str = self.channel["items"][0]["statistics"]["videoCount"]
        self.url: str = f'https://www.youtube.com/channel/{self.__channel_id}'
        self.description: str = self.channel['items'][0]['snippet']['description']
        self.subscriber_count: str = self.channel["items"][0]["statistics"]['subscriberCount']
        self.view_count: str = self.channel["items"][0]["statistics"]['viewCount']

    def __repr__(self):
        """
        Возвращает текстовое представление объекта полезное для отладки
        в виде названия класса и его атрибутов.
        """
        return (f'{self.__class__.__name__}({self.__channel_id}, {self.title}, {self.video_count}, {self.url},'
                f'{self.description}, {self.subscriber_count}, {self.view_count})')

    def __str__(self):
        """Возвращает строковое представление объекта."""
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        """Складывает количество подписчиков двух экземпляров."""
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        """
        Вычитает количество подписчиков одного экземпляра
        из количества подписчиков другого.
        """
        return int(other.subscriber_count) - int(self.subscriber_count)

    def __gt__(self, other):
        """
        Реализует оператор сравнения больше.
        Сравнивает количество подписчиков одного экземпляра с другим.
        """
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other):
        """
        Реализует оператор сравнения больше или равно.
        Сравнивает количество подписчиков одного экземпляра с другим.
        """
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def __lt__(self, other):
        """
        Реализует оператор сравнения меньше.
        Сравнивает количество подписчиков одного экземпляра с другим.
        """
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other):
        """
        Реализует оператор сравнения меньше или равно.
        Сравнивает количество подписчиков одного экземпляра с другим.
        """
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __eq__(self, other):
        """
        Реализует оператор сравнения равенства.
        Сравнивает количество подписчиков одного экземпляра с другим.
        """
        return int(self.subscriber_count) == int(other.subscriber_count)

    @property
    def channel_id(self):
        """Геттер для id канала."""
        return self.__channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """Класс-метод, возвращающий объект для работы с YouTube API."""
        youtube = build('youtube', 'v3', developerKey=cls.api_key)
        return youtube

    def to_json(self, json_file):
        """Сохраняет в файл значения атрибутов экземпляра `Channel`."""
        state = {"channel_id": self.__channel_id, "title": self.title, "description": self.description, "url": self.url,
                 "subscriber_count": self.subscriber_count, "video_count": self.video_count,
                 "view_count": self.view_count}
        with open(json_file, 'w', encoding='utf-8') as outfile:
            json.dump(state, outfile, indent=4)
