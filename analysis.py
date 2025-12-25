# analysis.py
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any
from models import Book


def books_to_dataframe(books: List[Book]) -> pd.DataFrame:
    """Преобразует список книг в pandas DataFrame."""
    if not books:
        return pd.DataFrame(columns=[
            "title", "author", "genre", "isbn", "status",
            "start_date", "end_date", "pages"
        ])
    data = [book.to_dict() for book in books]
    df = pd.DataFrame(data)
    return df


def analyze_reading_stats(books: List[Book]) -> Dict[str, Any]:
    """
    Анализирует статистику чтения.

    Возвращает словарь с ключами:
        - total_books
        - finished_books
        - reading_books
        - top_genres (топ-5 жанров среди прочитанных)
        - books_by_year (количество прочитанных книг по годам)
        - avg_reading_days (среднее время чтения в днях)
    """
    df = books_to_dataframe(books)

    # Общее количество
    total_books = len(df)
    # ЯВНО создаём копию, чтобы избежать SettingWithCopyWarning
    finished_books = df[df["status"] == "finished"].copy()
    reading_books = df[df["status"] == "reading"]

    # Топ-5 жанров (только для прочитанных)
    top_genres = {}
    if not finished_books.empty:
        genre_series = finished_books["genre"].dropna().str.split(", ").explode()
        top_genres = genre_series.value_counts().head(5).to_dict()

    # Книги по годам окончания
    books_by_year = {}
    if not finished_books.empty and finished_books["end_date"].notna().any():
        # Безопасное добавление столбца — теперь у нас копия
        finished_books["end_year"] = pd.to_datetime(
            finished_books["end_date"], errors="coerce"
        ).dt.year
        books_by_year = finished_books["end_year"].value_counts().sort_index().to_dict()

    # Среднее время чтения (в днях)
    avg_reading_days = None
    if not finished_books.empty:
        # Добавляем временные столбцы в копию — безопасно
        finished_books["start"] = pd.to_datetime(finished_books["start_date"], errors="coerce")
        finished_books["end"] = pd.to_datetime(finished_books["end_date"], errors="coerce")
        finished_books["duration"] = (finished_books["end"] - finished_books["start"]).dt.days
        valid_durations = finished_books["duration"].dropna()
        valid_durations = valid_durations[valid_durations >= 0]
        if not valid_durations.empty:
            avg_reading_days = int(valid_durations.mean())

    return {
        "total_books": total_books,
        "finished_books_count": len(finished_books),
        "reading_books_count": len(reading_books),
        "top_genres": top_genres,
        "books_by_year": books_by_year,
        "avg_reading_days": avg_reading_days
    }