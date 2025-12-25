# storage.py
import csv
import os
from typing import List
from models import Book

# Пути
DATA_DIR = "data"
BOOKS_FILE = os.path.join(DATA_DIR, "books.csv")

# Заголовки CSV (должны совпадать с ключами в Book.to_dict())
HEADERS = ["title", "author", "genre", "isbn", "status", "start_date", "end_date", "pages"]


def ensure_data_dir():
    """Создаёт директорию data/, если она не существует."""
    os.makedirs(DATA_DIR, exist_ok=True)


def save_books(books: List[Book]):
    """
    Сохраняет список книг в CSV-файл.

    Использует try/except для защиты от ошибок ввода-вывода.
    """
    ensure_data_dir()
    try:
        with open(BOOKS_FILE, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=HEADERS)
            writer.writeheader()
            for book in books:
                row = book.to_dict()
                # Заменяем None на пустую строку для корректного CSV
                for key in row:
                    if row[key] is None:
                        row[key] = ""
                writer.writerow(row)
    except (OSError, IOError) as e:
        print(f"❌ Ошибка записи файла: {e}")
    except Exception as e:
        print(f"❌ Неожиданная ошибка при сохранении: {e}")


def load_books() -> List[Book]:
    """
    Загружает книги из CSV-файла.

    Возвращает пустой список, если файл не существует или повреждён.
    """
    ensure_data_dir()
    if not os.path.exists(BOOKS_FILE):
        return []

    books = []
    try:
        with open(BOOKS_FILE, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            # Проверяем, что заголовки совпадают
            if set(reader.fieldnames) != set(HEADERS):
                print("⚠️  Формат CSV-файла не совпадает с ожидаемым.")
                return []

            for row in reader:
                # Преобразуем пустые строки обратно в None или int
                for key in ["isbn", "start_date", "end_date"]:
                    if row[key] == "":
                        row[key] = None
                if row["pages"] == "":
                    row["pages"] = None
                else:
                    try:
                        row["pages"] = int(row["pages"])
                    except (ValueError, TypeError):
                        row["pages"] = None

                books.append(Book.from_dict(row))
    except (OSError, IOError) as e:
        print(f"❌ Ошибка чтения файла: {e}")
        return []
    except Exception as e:
        print(f"❌ Ошибка при загрузке данных: {e}")
        return []

    return books