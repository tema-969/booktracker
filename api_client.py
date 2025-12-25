# api_client.py
import aiohttp
import asyncio
from typing import Optional, Dict, Any

# URL Open Library API
OPEN_LIBRARY_URL = "https://openlibrary.org/api/books"


async def fetch_book_by_isbn(isbn: str) -> Optional[Dict[str, Any]]:
    """
    Асинхронно получает данные книги по ISBN из Open Library API.

    Возвращает словарь с ключами:
        - title (str)
        - author (str)
        - genre (str)
        - pages (int, optional)

    Пример:
        await fetch_book_by_isbn("9780140449266")
        → {
            "title": "Anna Karenina",
            "author": "Leo Tolstoy",
            "genre": "Fiction, Classics",
            "pages": 864
        }

    Возвращает None в случае ошибки или отсутствия данных.
    """
    if not isbn or not isbn.strip():
        return None

    # Формируем bibkey
    bibkey = f"ISBN:{isbn.replace('-', '').replace(' ', '')}"
    params = {
        "bibkeys": bibkey,
        "format": "json",
        "jscmd": "data"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    OPEN_LIBRARY_URL,
                    params=params,
                    timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status != 200:
                    return None
                json_data = await response.json()

                book_data = json_data.get(bibkey)
                if not book_data:
                    return None

                # Извлечение данных
                title = book_data.get("title", "").strip()
                authors = book_data.get("authors", [])
                author_names = [a.get("name", "") for a in authors if a.get("name")]
                author = ", ".join(author_names) if author_names else "Unknown"

                # Жанры (subjects)
                subjects = book_data.get("subjects", [])
                genre_list = []
                for subj in subjects:
                    if isinstance(subj, dict) and "name" in subj:
                        genre_list.append(subj["name"])
                    elif isinstance(subj, str):
                        genre_list.append(subj)
                genre = ", ".join(genre_list[:3]) if genre_list else "Unknown"

                # Страницы
                pages = book_data.get("number_of_pages")
                if pages is not None:
                    try:
                        pages = int(pages)
                    except (ValueError, TypeError):
                        pages = None

                return {
                    "title": title,
                    "author": author,
                    "genre": genre,
                    "pages": pages
                }

    except asyncio.TimeoutError:
        print("⚠️  Тайм-аут при запросе к Open Library API")
        return None
    except aiohttp.ClientError as e:
        print(f"⚠️  Ошибка сети при запросе: {e}")
        return None
    except Exception as e:
        print(f"⚠️  Неожиданная ошибка в API-клиенте: {e}")
        return None