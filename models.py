# models.py
from datetime import datetime
from typing import Optional


class Book:
    """
    Представляет книгу в трекере чтения.

    Атрибуты:
        title (str): Название книги
        author (str): Автор
        genre (str): Жанр
        isbn (str, optional): ISBN (10 или 13 цифр)
        status (str): 'planned', 'reading', 'finished', 'paused'
        start_date (str, optional): Дата начала чтения (YYYY-MM-DD)
        end_date (str, optional): Дата окончания (YYYY-MM-DD)
        pages (int, optional): Количество страниц
    """

    def __init__(
            self,
            title: str,
            author: str,
            genre: str,
            isbn: Optional[str] = None,
            status: str = "planned",
            start_date: Optional[str] = None,
            end_date: Optional[str] = None,
            pages: Optional[int] = None
    ):
        self.title = title
        self.author = author
        self.genre = genre
        self.isbn = isbn
        self.status = status
        self.start_date = start_date
        self.end_date = end_date
        self.pages = pages

    def to_dict(self) -> dict:
        """Преобразует объект в словарь для сохранения в CSV/JSON."""
        return {
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "isbn": self.isbn,
            "status": self.status,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "pages": self.pages
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Создаёт объект Book из словаря."""
        return cls(**data)

    def __repr__(self):
        return f"<Book: {self.title} by {self.author}>"